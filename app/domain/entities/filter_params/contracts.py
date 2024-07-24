from dataclasses import dataclass

from app.domain.value_objects.student_id import StudentIdVO


@dataclass
class ContractsFilterParams:
    student_id: StudentIdVO | None
    html_content: str | None
    with_deleted: bool
