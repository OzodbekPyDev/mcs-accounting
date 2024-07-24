from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.dto.contract_templates import ContractTemplateResponse
from app.domain.entities.contracts import (ContractDownloadEntity,
                                           ContractEntity,)


@dataclass
class CreateContractRequest:
    language: str
    created_by: UUID
    student_data: dict


@dataclass
class UpdateContractRequest:
    id: UUID
    template_id: UUID
    html_content: str
    start_date: datetime
    first_payment_due_date: datetime
    expiration_date: datetime
    education_years: str
    is_archived: bool
    updated_by: UUID


@dataclass
class StudentContractInfoResponse:
    id: UUID
    student_id: UUID
    file_id: UUID

    @classmethod
    def from_entity(
        cls, entity: ContractDownloadEntity | ContractEntity
    ) -> "StudentContractInfoResponse":
        return cls(
            id=entity.id.value,
            student_id=entity.student_id.value,
            file_id=entity.file_id.value,
        )


@dataclass
class ContractResponse:
    id: UUID
    student_id: UUID
    template: ContractTemplateResponse
    html_content: str
    number: str
    download_counter: int
    start_date: datetime
    first_payment_due_date: datetime
    expiration_date: datetime
    education_years: str
    last_downloaded_at: datetime
    is_archived: bool
    file_id: UUID
    created_at: datetime
    created_by: UUID
    updated_at: datetime | None
    updated_by: UUID | None

    @classmethod
    def from_entity(cls, entity: ContractEntity) -> "ContractResponse":
        return cls(
            id=entity.id.value,
            student_id=entity.student_id.value,
            template=ContractTemplateResponse.from_entity(entity.template),
            html_content=entity.html_content,
            number=entity.number,
            download_counter=entity.download_counter,
            start_date=entity.start_date,
            first_payment_due_date=entity.first_payment_due_date,
            expiration_date=entity.expiration_date,
            education_years=entity.education_years,
            last_downloaded_at=entity.last_downloaded_at,
            is_archived=entity.is_archived,
            file_id=entity.file_id.value,
            created_at=entity.created_at,
            created_by=entity.created_by.value,
            updated_at=entity.updated_at,
            updated_by=entity.updated_by.value,
        )


@dataclass
class GetListContractsRequest:
    student_id: UUID | None = None
    html_content: str | None = None
    with_deleted: bool = False
