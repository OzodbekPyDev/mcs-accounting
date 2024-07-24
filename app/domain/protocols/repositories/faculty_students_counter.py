from typing import Protocol

from app.domain.entities.faculty_students_counter import \
    FacultyStudentCounterEntity
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO


class IFacultyStudentsCounterRepository(Protocol):
    async def create(self, data: FacultyStudentCounterEntity) -> None:
        raise NotImplementedError

    async def get_by_faculty_id_and_education_years(
        self,
        faculty_id: FacultyIdVO,
        education_years: str,
    ) -> FacultyStudentCounterEntity | None:
        raise NotImplementedError

    async def update_quantity(self, id: IdVO, quantity: int) -> None:
        raise NotImplementedError
