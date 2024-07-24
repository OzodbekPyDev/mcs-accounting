from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.value_objects.faculty_id import FacultyIdVO


@dataclass
class FacultyStudentCounterEntity(BaseEntity):
    faculty_id: FacultyIdVO
    education_years: str
    quantity: int

    def increment_quantity(self) -> None:
        self.quantity += 1
