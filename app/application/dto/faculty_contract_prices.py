from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.faculty_contract_prices import \
    FacultyContractPriceEntity


@dataclass
class CreateFacultyContractPriceRequest:
    faculty_id: UUID
    amount: int
    transcriptions: dict[str, str]
    created_by: UUID


@dataclass
class UpdateFacultyContractPriceRequest:
    id: UUID
    faculty_id: UUID
    amount: int
    transcriptions: dict[str, str]
    updated_by: UUID


@dataclass
class DeleteFacultyContractPriceRequest:
    id: UUID
    deleted_by: UUID


@dataclass
class FacultyContractPriceResponse:
    id: UUID
    faculty_id: UUID
    amount: int
    transcriptions: dict[str, str]
    created_by: UUID
    updated_by: UUID | None
    deleted_by: UUID | None
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    @classmethod
    def from_entity(
        cls, entity: FacultyContractPriceEntity
    ) -> "FacultyContractPriceResponse":
        return cls(
            id=entity.id.value,
            faculty_id=entity.faculty_id.value,
            amount=entity.amount,
            transcriptions=entity.transcriptions,
            created_by=entity.created_by.value,
            updated_by=entity.updated_by.value,
            deleted_by=entity.deleted_by.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )


@dataclass
class GetAllFacultyContractPricesRequest:
    with_deleted: bool = False
