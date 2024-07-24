from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.faculty_students_counter import \
    FacultyStudentCounterEntity
from app.domain.protocols.repositories.faculty_students_counter import \
    IFacultyStudentsCounterRepository
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm.faculty_students_counter import \
    FacultyStudentCounter


class SqlalchemyFacultyStudentsCounterRepository(IFacultyStudentsCounterRepository):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: FacultyStudentCounterEntity) -> None:
        stmt = insert(FacultyStudentCounter).values(
            id=data.id.value,
            faculty_id=data.faculty_id.value,
            education_years=data.education_years,
            quantity=data.quantity,
            created_at=data.created_at,
        )
        await self.session.execute(stmt)

    async def get_by_faculty_id_and_education_years(
        self,
        faculty_id: FacultyIdVO,
        education_years: str,
    ) -> FacultyStudentCounterEntity | None:
        stmt = select(FacultyStudentCounter).where(
            FacultyStudentCounter.faculty_id == faculty_id.value,
            FacultyStudentCounter.education_years == education_years,
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_entity() if item else None

    async def update_quantity(self, id: IdVO, quantity: int) -> None:
        stmt = (
            update(FacultyStudentCounter)
            .where(FacultyStudentCounter.id == id.value)
            .values(
                quantity=quantity,
            )
        )
        await self.session.execute(stmt)
