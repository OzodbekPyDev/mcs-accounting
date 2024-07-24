from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class BranchIdVO:
    value: UUID
