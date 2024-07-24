from app.application.protocols.interactor import Interactor
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.protocols.repositories.uow import IUnitOfWork


class DeleteAllPayments(Interactor[None, None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        payments_repository: IPaymentsRepository,
    ) -> None:
        self.uow = uow
        self.payments_repository = payments_repository

    async def __call__(self, request: None) -> None:
        await self.payments_repository.delete_all()
        await self.uow.commit()
