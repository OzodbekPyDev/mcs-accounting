from dataclasses import dataclass

from app.domain.value_objects.branch_id import BranchIdVO


@dataclass
class ContractTemplatesFilterParams:
    branch_id: BranchIdVO | None
    degree_program: str | None
    language: str | None
    is_active: bool
    with_deleted: bool | None
