from app.application.dto.contract_templates import (
    ContractTemplateResponse, UpdateContractTemplateRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.exceptions.contract_templates import \
    ContractTemplateNotFoundException
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import UpdatedByVO
from app.domain.value_objects.id import IdVO


class UpdateContractTemplate(
    Interactor[UpdateContractTemplateRequest, ContractTemplateResponse]
):

    def __init__(
        self,
        uow: IUnitOfWork,
        contract_templates_repository: IContractTemplatesRepository,
        datetime_provider: DateTimeProvider,
    ):
        self.uow = uow
        self.contract_templates_repository = contract_templates_repository
        self.datetime_provider = datetime_provider

    async def __call__(
        self, request: UpdateContractTemplateRequest
    ) -> ContractTemplateResponse:
        cont_temp_entity = await self.contract_templates_repository.get_by_id(
            id=IdVO(value=request.id)
        )
        if not cont_temp_entity:
            raise ContractTemplateNotFoundException("Contract template not found")

        cont_temp_entity.update(
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
            updated_at=self.datetime_provider.get_current_time(),
            updated_by=UpdatedByVO(value=request.updated_by),
        )

        await self.contract_templates_repository.update(cont_temp_entity)
        await self.uow.commit()
        return ContractTemplateResponse.from_entity(cont_temp_entity)
