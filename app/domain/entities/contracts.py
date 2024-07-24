from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity
from app.domain.entities.contract_templates import ContractTemplateEntity
from app.domain.entities.mixins.admin_mixin import AdminMixinEntity
from app.domain.value_objects.created_updated_by import UpdatedByVO
from app.domain.value_objects.file_id import FileIdVO
from app.domain.value_objects.id import IdVO
from app.domain.value_objects.student_id import StudentIdVO


@dataclass
class ContractEntity(BaseEntity, AdminMixinEntity):
    student_id: StudentIdVO
    template_id: IdVO
    template: ContractTemplateEntity
    html_content: str
    number: str
    download_counter: int
    start_date: datetime
    first_payment_due_date: datetime
    expiration_date: datetime
    education_years: str
    last_downloaded_at: datetime
    is_archived: bool
    file_id: FileIdVO

    def update(
        self,
        template_id: IdVO,
        html_content: str,
        start_date: datetime,
        first_payment_due_date: datetime,
        expiration_date: datetime,
        education_years: str,
        is_archived: bool,
        updated_at: datetime,
        updated_by: UpdatedByVO,
    ) -> None:
        self.template_id = template_id
        self.html_content = html_content
        self.start_date = start_date
        self.first_payment_due_date = first_payment_due_date
        self.expiration_date = expiration_date
        self.education_years = education_years
        self.is_archived = is_archived
        self.updated_at = updated_at
        self.updated_by = updated_by


@dataclass
class ContractDownloadEntity:
    id: IdVO
    student_id: StudentIdVO
    file_id: FileIdVO
    download_counter: int
    last_downloaded_at: datetime

    def update(self, last_downloaded_at: datetime) -> None:
        self.last_downloaded_at = last_downloaded_at

    def increment_download_counter(self):
        self.download_counter += 1
