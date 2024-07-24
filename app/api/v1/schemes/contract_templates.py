from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UpdateContractTemplateSchema:
    branch_id: UUID
    degree_program: str
    language: str
    info: str
    name: str
    html_content: str
    is_active: bool
    start_date: datetime
    first_payment_due_date: datetime
    expiration_date: datetime
    education_years: str
    updated_by: UUID


@dataclass
class DeleteContractTemplateSchema:
    deleted_by: UUID
