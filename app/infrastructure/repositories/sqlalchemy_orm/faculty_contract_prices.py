from datetime import datetime

from asyncpg import UniqueViolationError
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.faculty_contract_prices import \
    FacultyContractPriceEntity
from app.domain.entities.filter_params.faculty_contract_prices import \
    FacultyContractPricesFilterParams
from app.domain.exceptions.constraints import UniqueConstraintsException
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm.faculty_contract_prices import \
    FacultyContractPrice


class SqlalchemyFacultyContractPricesRepository(IFacultyContractPricesRepository):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: FacultyContractPriceEntity) -> None:
        try:
            stmt = insert(FacultyContractPrice).values(
                id=data.id.value,
                faculty_id=data.faculty_id.value,
                amount=data.amount,
                transcriptions=data.transcriptions,
                created_by=data.created_by.value,
                updated_by=data.updated_by.value,
                created_at=data.created_at,
            )
            await self.session.execute(stmt)
        except UniqueViolationError:
            raise UniqueConstraintsException(
                "Faculty contract price already exists. (UniqueViolationError)"
            )

    async def get_all(
        self, filter_params: FacultyContractPricesFilterParams
    ) -> list[FacultyContractPriceEntity]:
        query = select(FacultyContractPrice)

        if not filter_params.with_deleted:
            query = query.filter(FacultyContractPrice.deleted_at.is_(None))

        result = await self.session.execute(query)
        items = result.scalars().all()

        return [item.to_entity() for item in items]

    async def get_by_id(self, id: IdVO) -> FacultyContractPriceEntity | None:
        stmt = select(FacultyContractPrice).where(FacultyContractPrice.id == id.value)
        result = await self.session.execute(stmt)
        item = result.scalar()

        return item.to_entity() if item else None

    async def update(self, data: FacultyContractPriceEntity) -> None:
        stmt = (
            update(FacultyContractPrice)
            .where(FacultyContractPrice.id == data.id.value)
            .values(
                faculty_id=data.faculty_id.value,
                amount=data.amount,
                transcriptions=data.transcriptions,
                updated_by=data.updated_by.value,
                updated_at=data.updated_at,
            )
        )
        await self.session.execute(stmt)

    async def delete(
        self, id: IdVO, deleted_by: DeletedByVO, deleted_at: datetime
    ) -> None:
        stmt = (
            update(FacultyContractPrice)
            .where(
                FacultyContractPrice.id == id.value,
                FacultyContractPrice.deleted_at.is_(None),
            )
            .values(deleted_by=deleted_by.value, deleted_at=deleted_at)
        )
        await self.session.execute(stmt)

    async def get_by_faculty_id(
        self, faculty_id: FacultyIdVO
    ) -> FacultyContractPriceEntity | None:
        stmt = select(FacultyContractPrice).where(
            FacultyContractPrice.faculty_id == faculty_id.value
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()

        return item.to_entity() if item else None
