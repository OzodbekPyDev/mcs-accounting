from app.application.dto.contract_templates import \
    DeleteContractTemplateRequest
from app.application.protocols.interactor import Interactor
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.id import IdVO


class DeleteContractTemplate(Interactor[DeleteContractTemplateRequest, None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        contract_templates_repository: IContractTemplatesRepository,
        datetime_provider: DateTimeProvider,
    ):
        self.uow = uow
        self.contract_templates_repository = contract_templates_repository
        self.datetime_provider = datetime_provider

    async def __call__(self, request: DeleteContractTemplateRequest) -> None:
        await self.contract_templates_repository.delete(
            id=IdVO(value=request.id),
            deleted_by=DeletedByVO(value=request.deleted_by),
            deleted_at=self.datetime_provider.get_current_time(),
        )
        await self.uow.commit()
