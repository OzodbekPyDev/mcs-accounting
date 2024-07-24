from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreatedByVO:
    value: UUID


@dataclass(frozen=True)
class UpdatedByVO:
    value: UUID | None


@dataclass(frozen=True)
class DeletedByVO:
    value: UUID | None
