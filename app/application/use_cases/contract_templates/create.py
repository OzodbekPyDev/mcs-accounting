from app.application.dto.contract_templates import (
    ContractTemplateResponse, CreateContractTemplateRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.entities.contract_templates import ContractTemplateEntity
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)
from app.domain.value_objects.id import IdVO


class CreateContractTemplate(
    Interactor[CreateContractTemplateRequest, ContractTemplateResponse]
):

    def __init__(
        self,
        uow: IUnitOfWork,
        contract_templates_repository: IContractTemplatesRepository,
        id_provider: IdProvider,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.contract_templates_repository = contract_templates_repository
        self.id_provider = id_provider
        self.datetime_provider = datetime_provider

    async def __call__(
        self, request: CreateContractTemplateRequest
    ) -> ContractTemplateResponse:
        cont_temp_entity = ContractTemplateEntity(
            id=IdVO(value=self.id_provider.generate_uuid()),
            created_at=self.datetime_provider.get_current_time(),
            updated_at=None,
            deleted_at=None,
            branch_id=BranchIdVO(value=request.branch_id),
            degree_program=request.degree_program,
            language=request.language,
            info=request.info,
            name=request.name,
            html_content=request.html_content,
            is_active=request.is_active,
            start_date=request.start_date,
            first_payment_due_date=request.first_payment_due_date,
            expiration_date=request.expiration_date,
            education_years=request.education_years,
            created_by=CreatedByVO(value=request.created_by),
            updated_by=UpdatedByVO(value=None),
            deleted_by=DeletedByVO(value=None),
        )
        await self.contract_templates_repository.create(cont_temp_entity)
        await self.uow.commit()
        return ContractTemplateResponse.from_entity(cont_temp_entity)
