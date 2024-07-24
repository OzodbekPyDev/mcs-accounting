from uuid import UUID

from app.application.dto.contracts import (ContractResponse,
                                           UpdateContractRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.exceptions.contracts import ContractNotFoundException
from app.domain.exceptions.pdf_generation import PdfFileNotGeneratedException
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.docs_microservice_provider import \
    IDocsMicroserviceProvider
from app.domain.protocols.adapters.file_manager import FileManager
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.created_updated_by import UpdatedByVO
from app.domain.value_objects.id import IdVO


class UpdateContract(Interactor[UpdateContractRequest, ContractResponse]):

    def __init__(
        self,
        uow: IUnitOfWork,
        contracts_repository: IContractsRepository,
        datetime_provider: DateTimeProvider,
        docs_microservice_provider: IDocsMicroserviceProvider,
        file_manager: FileManager,
    ) -> None:
        self.uow = uow
        self.contracts_repository = contracts_repository
        self.datetime_provider = datetime_provider
        self.docs_microservice_provider = docs_microservice_provider
        self.file_manager = file_manager

    async def __call__(self, request: UpdateContractRequest) -> ContractResponse:
        contract_entity = await self.contracts_repository.get_by_id(
            IdVO(value=request.id)
        )

        if not contract_entity:
            raise ContractNotFoundException("Contract not found")

        if contract_entity.html_content != request.html_content:
            binary_code_pdf = self.file_manager.generate_binary_code_of_pdf_file(
                html_content=request.html_content
            )
            # binary_code_pdf = pdfkit.from_string(request.html_content, output_path=False)
            if not binary_code_pdf:
                raise PdfFileNotGeneratedException(
                    "PDF file not generated, something went wrong"
                )
            await self.docs_microservice_provider.update_file(
                key=contract_entity.file_id.value,
                filename="contract.pdf",
                content=binary_code_pdf,
            )

        contract_entity.update(
            template_id=IdVO(request.template_id),
            html_content=request.html_content,
            start_date=request.start_date,
            first_payment_due_date=request.first_payment_due_date,
            expiration_date=request.expiration_date,
            education_years=request.education_years,
            is_archived=request.is_archived,
            updated_at=self.datetime_provider.get_current_time(),
            updated_by=UpdatedByVO(value=request.updated_by),
        )

        await self.contracts_repository.update(contract_entity)
        await self.uow.commit()

        return ContractResponse.from_entity(contract_entity)


class UpdateContractDownloadDetails(Interactor[UUID, None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        contracts_repository: IContractsRepository,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.contracts_repository = contracts_repository
        self.datetime_provider = datetime_provider

    async def __call__(self, request: UUID) -> None:

        contract_entity = await self.contracts_repository.get_student_active_contract_key_details_to_download(
            id=IdVO(value=request),
            current_datetime=self.datetime_provider.get_current_time(),
        )

        if not contract_entity:
            raise ContractNotFoundException(
                "Contract not found, probably it is not available."
            )

        contract_entity.update(
            last_downloaded_at=self.datetime_provider.get_current_time(),
        )
        contract_entity.increment_download_counter()

        await self.contracts_repository.update_contract_download_details(
            id=contract_entity.id,
            last_downloaded_at=contract_entity.last_downloaded_at,
            download_counter=contract_entity.download_counter,
        )
        await self.uow.commit()
