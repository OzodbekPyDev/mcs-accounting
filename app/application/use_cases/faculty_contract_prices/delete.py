from app.application.dto.faculty_contract_prices import \
    DeleteFacultyContractPriceRequest
from app.application.protocols.interactor import Interactor
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.id import IdVO


class DeleteFacultyContractPrice(Interactor[DeleteFacultyContractPriceRequest, None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        faculty_contract_prices_repository: IFacultyContractPricesRepository,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.faculty_contract_prices_repository = faculty_contract_prices_repository
        self.datetime_provider = datetime_provider

    async def __call__(self, request: DeleteFacultyContractPriceRequest) -> None:
        await self.faculty_contract_prices_repository.delete(
            id=IdVO(value=request.id),
            deleted_by=DeletedByVO(value=request.deleted_by),
            deleted_at=self.datetime_provider.get_current_time(),
        )
        await self.uow.commit()
