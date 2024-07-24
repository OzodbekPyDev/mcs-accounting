from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateFacultyContractPriceSchema:
    faculty_id: UUID
    amount: int
    transcriptions: dict[str, str]
    updated_by: UUID


@dataclass
class DeleteFacultyContractPriceSchema:
    deleted_by: UUID
