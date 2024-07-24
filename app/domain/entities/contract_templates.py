from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity
from app.domain.entities.mixins.admin_mixin import AdminMixinEntity
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import UpdatedByVO


@dataclass
class ContractTemplateEntity(BaseEntity, AdminMixinEntity):
    branch_id: BranchIdVO
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

    def update(
        self,
        branch_id: BranchIdVO,
        degree_program: str,
        language: str,
        info: str,
        name: str,
        html_content: str,
        is_active: bool,
        start_date: datetime,
        first_payment_due_date: datetime,
        expiration_date: datetime,
        education_years: str,
        updated_at: datetime,
        updated_by: UpdatedByVO,
    ) -> None:
        self.branch_id = branch_id
        self.degree_program = degree_program
        self.language = language
        self.info = info
        self.name = name
        self.html_content = html_content
        self.is_active = is_active
        self.start_date = start_date
        self.first_payment_due_date = first_payment_due_date
        self.expiration_date = expiration_date
        self.education_years = education_years
        self.updated_at = updated_at
        self.updated_by = updated_by
