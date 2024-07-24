from datetime import datetime
from uuid import UUID

from sqlalchemy import Index, text
from sqlalchemy.orm import Mapped

from app.domain.entities.contract_templates import ContractTemplateEntity
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm.base import Base
from app.infrastructure.db.models.sqlalchemy_orm.mixins.admin_mixin import \
    AdminMixin


class ContractTemplate(Base, AdminMixin):
    __tablename__ = "contract_templates"
    __table_args__ = (
        # Создаем частичный уникальный индекс, который работает только для активных шаблонов
        Index(
            "ix_active_contracts",
            "branch_id",
            "degree_program",
            "language",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    branch_id: Mapped[UUID]
    degree_program: Mapped[str]
    language: Mapped[str]
    info: Mapped[str]
    name: Mapped[str]
    html_content: Mapped[str]
    is_active: Mapped[bool]
    start_date: Mapped[datetime]
    first_payment_due_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    education_years: Mapped[str]

    def to_entity(self) -> ContractTemplateEntity:
        return ContractTemplateEntity(
            id=IdVO(self.id),
            branch_id=BranchIdVO(self.branch_id),
            degree_program=self.degree_program,
            language=self.language,
            info=self.info,
            name=self.name,
            html_content=self.html_content,
            is_active=self.is_active,
            start_date=self.start_date,
            first_payment_due_date=self.first_payment_due_date,
            expiration_date=self.expiration_date,
            education_years=self.education_years,
            created_by=CreatedByVO(self.created_by),
            updated_by=UpdatedByVO(self.updated_by),
            deleted_by=DeletedByVO(self.deleted_by),
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )
