from enum import Enum
from typing import Protocol


class EducationTypeSuffix(str, Enum):
    full_time = ""
    evening_time = "E"
    extramural = "P"


class ContractNumberProvider(Protocol):
    def generate_contract_number(
        self,
        year: int,
        branch_suffix: str,
        faculty_suffix: str,
        edu_type_suffix: str,
        quantity: int,
        course_number: int,
    ) -> str:
        raise NotImplementedError
