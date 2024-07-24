from datetime import datetime

from app.application.dto.contracts import (CreateContractRequest,
                                           StudentContractInfoResponse,)
from app.application.protocols.interactor import Interactor
from app.domain.entities.contracts import ContractEntity
from app.domain.entities.faculty_students_counter import \
    FacultyStudentCounterEntity
from app.domain.exceptions.contract_templates import \
    ContractTemplateNotFoundException
from app.domain.exceptions.contracts import StudentAlreadyHasContractException
from app.domain.exceptions.faculty_contract_prices import \
    FacultyContractPriceNotFoundException
from app.domain.exceptions.pdf_generation import PdfFileNotGeneratedException
from app.domain.protocols.adapters.contract_number_provider import (
    ContractNumberProvider, EducationTypeSuffix,)
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.docs_microservice_provider import \
    IDocsMicroserviceProvider
from app.domain.protocols.adapters.file_manager import FileManager
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.faculty_students_counter import \
    IFacultyStudentsCounterRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.file_id import FileIdVO
from app.domain.value_objects.id import IdVO
from app.domain.value_objects.student_id import StudentIdVO


class CreateContract(Interactor[CreateContractRequest, StudentContractInfoResponse]):

    def __init__(
        self,
        uow: IUnitOfWork,
        contracts_repository: IContractsRepository,
        contract_templates_repository: IContractTemplatesRepository,
        faculty_students_counter_repository: IFacultyStudentsCounterRepository,
        faculty_contract_prices_repository: IFacultyContractPricesRepository,
        id_provider: IdProvider,
        datetime_provider: DateTimeProvider,
        contract_number_provider: ContractNumberProvider,
        docs_microservice_provider: IDocsMicroserviceProvider,
        file_manager: FileManager,
    ) -> None:
        self.uow = uow
        self.contracts_repository = contracts_repository
        self.contract_templates_repository = contract_templates_repository
        self.faculty_students_counter_repository = faculty_students_counter_repository
        self.faculty_contract_prices_repository = faculty_contract_prices_repository
        self.id_provider = id_provider
        self.datetime_provider = datetime_provider
        self.contract_number_provider = contract_number_provider
        self.docs_microservice_provider = docs_microservice_provider
        self.file_manager = file_manager

    async def __call__(
        self, request: CreateContractRequest
    ) -> StudentContractInfoResponse:
        """CREATE A VARIABLE TO STORE THE CURRENT TIME"""
        current_datetime = self.datetime_provider.get_current_time()

        """CHECK IF THE STUDENT HAS A CONTRACT IN THE CURRENT EDUCATION YEAR"""
        has_contract_in_current_education_year = (
            await self.contracts_repository.has_contract_in_current_education_year(
                student_id=StudentIdVO(value=request.student_data["id"]),
                current_datetime=current_datetime,
            )
        )

        if has_contract_in_current_education_year:
            raise StudentAlreadyHasContractException(
                "Student already has the contract in current education year!"
            )

        """
        IF THERE IS NO ACTIVE CONTRACT,
        FIRSTLY FIND AN APPROPRIATE TEMPLATE
        """
        contract_template_entity = await self.contract_templates_repository.get_appropriate_contract_template_or_none(
            branch_id=BranchIdVO(
                request.student_data["group"]["faculty"]["branch"]["id"]
            ),
            degree_program=request.student_data["group"]["faculty"]["degree"],
            language=request.language,
            current_datetime=current_datetime,
        )

        if not contract_template_entity:
            raise ContractTemplateNotFoundException(
                "Could not find an appropriate contract template."
            )

        """GET/CREATE A FACULTY STUDENTS COUNTER IN ORDER TO CREATE A CONTRACT NUMBER"""
        faculty_students_counter_entity = (
            await self._get_or_create_faculty_students_counter(
                faculty_id=FacultyIdVO(request.student_data["group"]["faculty"]["id"]),
                current_datetime=current_datetime,
                education_years=contract_template_entity.education_years,
            )
        )

        """GENERATE A CONTACT NUMBER"""
        contract_number = self.contract_number_provider.generate_contract_number(
            year=current_datetime.year,
            branch_suffix=request.student_data["group"]["faculty"]["branch"]["name"][
                "en"
            ][:3],
            faculty_suffix=request.student_data["group"]["faculty"]["suffix"],
            edu_type_suffix=EducationTypeSuffix[
                request.student_data["group"]["education_type"]
            ].value,
            quantity=faculty_students_counter_entity.quantity,
            course_number=request.student_data["group"]["course"],
        )

        """GET FACULTY CONTACT PRICE"""
        faculty_contract_price = (
            await (
                self.faculty_contract_prices_repository.get_by_faculty_id(
                    faculty_id=FacultyIdVO(
                        request.student_data["group"]["faculty"]["id"]
                    )
                )
            )
        )
        if not faculty_contract_price:
            raise FacultyContractPriceNotFoundException(
                "Faculty contract price not found"
            )

        """GENERATE HTML CONTENT WITH STUDENT'S DATA"""
        rendered_html_content = self.file_manager.render_html_content(
            html_content=contract_template_entity.html_content,
            contract_number=contract_number,
            student_data=request.student_data,
        )

        """GENERATE BINARY CODE OF PDF FILE WITH HTML CONTENT"""
        binary_code_pdf = self.file_manager.generate_binary_code_of_pdf_file(
            html_content=rendered_html_content,
        )
        if not binary_code_pdf:
            raise PdfFileNotGeneratedException(
                "PDF file not generated, something went wrong"
            )

        """GENERATE FILE UUID_V6 CODE"""
        file_id = self.id_provider.generate_uuid_v6()

        """SEND BINARY CODE OF PDF TO DOCS MICROSERVICE"""
        await self.docs_microservice_provider.create_file(
            key=file_id, filename="contract.pdf", content=binary_code_pdf
        )

        """CREATE A CONTRACT ENTITY"""
        contract_entity = ContractEntity(
            id=IdVO(value=self.id_provider.generate_uuid()),
            created_at=current_datetime,
            created_by=CreatedByVO(value=request.created_by),
            updated_at=None,
            updated_by=UpdatedByVO(value=None),
            deleted_at=None,
            deleted_by=DeletedByVO(value=None),
            student_id=StudentIdVO(request.student_data["id"]),
            template_id=contract_template_entity.id,
            template=contract_template_entity,
            html_content=rendered_html_content,
            number=contract_number,
            download_counter=1,  # it should be since we are downloading it for the first time
            start_date=contract_template_entity.start_date,
            first_payment_due_date=contract_template_entity.first_payment_due_date,
            expiration_date=contract_template_entity.expiration_date,
            education_years=contract_template_entity.education_years,
            last_downloaded_at=current_datetime,
            is_archived=False,
            file_id=FileIdVO(file_id),
        )
        await self.contracts_repository.create(contract_entity)
        await self.uow.commit()
        return StudentContractInfoResponse.from_entity(contract_entity)

    async def _get_or_create_faculty_students_counter(
        self, faculty_id: FacultyIdVO, current_datetime: datetime, education_years: str
    ) -> FacultyStudentCounterEntity:
        """GET/CREATE A FACULTY STUDENTS COUNTER IN ORDER TO CREATE A CONTRACT NUMBER"""
        faculty_students_counter_entity = await self.faculty_students_counter_repository.get_by_faculty_id_and_education_years(
            faculty_id=faculty_id, education_years=education_years
        )

        if not faculty_students_counter_entity:
            faculty_students_counter_entity = FacultyStudentCounterEntity(
                id=IdVO(value=self.id_provider.generate_uuid()),
                faculty_id=faculty_id,
                education_years=education_years,
                quantity=0,  # naq - it should be 0, we will increment it later
                created_at=current_datetime,
                updated_at=None,
                deleted_at=None,
            )
            await self.faculty_students_counter_repository.create(
                data=faculty_students_counter_entity
            )

        """INCREMENT THE QUANTITY OF STUDENTS"""
        faculty_students_counter_entity.increment_quantity()

        await self.faculty_students_counter_repository.update_quantity(
            id=faculty_students_counter_entity.id,
            quantity=faculty_students_counter_entity.quantity,
        )

        return faculty_students_counter_entity
