from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.contract_templates import ContractTemplateEntity


@dataclass
class CreateContractTemplateRequest:
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
    created_by: UUID


@dataclass
class UpdateContractTemplateRequest:
    id: UUID
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
class DeleteContractTemplateRequest:
    id: UUID
    deleted_by: UUID


@dataclass
class ContractTemplateResponse:
    id: UUID
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
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    created_by: UUID
    updated_by: UUID | None
    deleted_by: UUID | None

    @classmethod
    def from_entity(cls, entity: ContractTemplateEntity) -> "ContractTemplateResponse":
        return cls(
            id=entity.id.value,
            branch_id=entity.branch_id.value,
            degree_program=entity.degree_program,
            language=entity.language,
            info=entity.info,
            name=entity.name,
            html_content=entity.html_content,
            is_active=entity.is_active,
            start_date=entity.start_date,
            first_payment_due_date=entity.first_payment_due_date,
            expiration_date=entity.expiration_date,
            education_years=entity.education_years,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
            created_by=entity.created_by.value,
            updated_by=entity.updated_by.value,
            deleted_by=entity.deleted_by.value,
        )


@dataclass
class GetListContractTemplatesRequest:
    branch_id: UUID | None = None
    degree_program: str | None = None
    language: str | None = None
    is_active: bool = None
    with_deleted: bool = False
