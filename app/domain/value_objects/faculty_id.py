from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class FacultyIdVO:
    value: UUID
