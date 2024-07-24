from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.protocols.repositories.uow import IUnitOfWork


class SqlalchemyUnitOfWork(IUnitOfWork):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
