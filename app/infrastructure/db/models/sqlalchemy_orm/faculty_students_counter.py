from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.domain.entities.faculty_students_counter import \
    FacultyStudentCounterEntity
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm import Base


class FacultyStudentCounter(Base):
    __tablename__ = "faculty_students_counter"

    education_years: Mapped[str]
    faculty_id: Mapped[UUID] = mapped_column(unique=True)
    quantity: Mapped[int]

    def to_entity(self) -> FacultyStudentCounterEntity:
        return FacultyStudentCounterEntity(
            id=IdVO(self.id),
            education_years=self.education_years,
            faculty_id=FacultyIdVO(self.faculty_id),
            quantity=self.quantity,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )
