from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.payments import PaymentEntity
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm.payments import Payment

from app.domain.entities.filter_params.payments import PaymentsFilterParams


class SqlalchemyPaymentsRepository(IPaymentsRepository):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_create(self, entities: list[PaymentEntity]) -> None:
        stmt = insert(Payment).values(
            [
                {
                    "id": entity.id.value,
                    "contract_number": entity.contract_number,
                    "full_name": entity.full_name,
                    "passport_number": entity.passport_number,
                    "pinfl": entity.pinfl,
                    "amount": entity.amount,
                    "created_at": entity.created_at,
                }
                for entity in entities
            ]
        )
        await self.session.execute(stmt)

    async def create(self, entity: PaymentEntity) -> None:
        stmt = insert(Payment).values(
            id=entity.id.value,
            contract_number=entity.contract_number,
            full_name=entity.full_name,
            passport_number=entity.passport_number,
            pinfl=entity.pinfl,
            amount=entity.amount,
            created_at=entity.created_at,
        )
        await self.session.execute(stmt)

    async def get_all(self, filter_params: PaymentsFilterParams) -> list[PaymentEntity]:
        stmt = select(Payment)

        if filter_params.passport_number:
            stmt = stmt.where(Payment.passport_number == filter_params.passport_number)

        if filter_params.contract_number:
            stmt = stmt.where(Payment.contract_number == filter_params.contract_number)

        if filter_params.pinfl:
            stmt = stmt.where(Payment.pinfl == filter_params.pinfl)

        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return [item.to_entity() for item in items]

    async def get_by_id(self, id: IdVO) -> PaymentEntity | None:
        stmt = select(Payment).where(Payment.id == id.value)
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_entity() if item else None

    async def get_by_contract_number(self, contract_number: str) -> PaymentEntity | None:
        stmt = select(Payment).where(
            Payment.contract_number == contract_number,
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_entity() if item else None

    async def update(self, entity: PaymentEntity) -> None:
        query = update(Payment).values(
            full_name=entity.full_name,
            pinfl=entity.pinfl,
            amount=entity.amount,
            updated_at=entity.updated_at,
        )
        await self.session.execute(query)

    async def delete_all(self) -> None:
        query = delete(Payment)
        await self.session.execute(query)
