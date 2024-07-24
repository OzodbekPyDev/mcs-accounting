from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.contracts import ContractEntity
from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)
from app.domain.value_objects.file_id import FileIdVO
from app.domain.value_objects.id import IdVO
from app.domain.value_objects.student_id import StudentIdVO
from app.infrastructure.db.models.sqlalchemy_orm import Base
from app.infrastructure.db.models.sqlalchemy_orm.mixins.admin_mixin import \
    AdminMixin


if TYPE_CHECKING:
    from app.infrastructure.db.models.sqlalchemy_orm.contract_templates import \
        ContractTemplate  # noqa


class Contract(Base, AdminMixin):
    __tablename__ = "contracts"

    student_id: Mapped[UUID]
    template_id: Mapped[UUID] = mapped_column(ForeignKey("contract_templates.id"))
    html_content: Mapped[str]
    number: Mapped[str] = mapped_column(unique=True)
    download_counter: Mapped[int]
    start_date: Mapped[datetime]
    first_payment_due_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    education_years: Mapped[str]
    last_downloaded_at: Mapped[datetime]
    is_archived: Mapped[bool]
    file_id: Mapped[UUID]

    template: Mapped["ContractTemplate"] = relationship()

    def to_entity(self) -> ContractEntity:
        return ContractEntity(
            id=IdVO(self.id),
            student_id=StudentIdVO(self.student_id),
            template_id=IdVO(self.template_id),
            template=self.template.to_entity(),
            html_content=self.html_content,
            number=self.number,
            download_counter=self.download_counter,
            start_date=self.start_date,
            first_payment_due_date=self.first_payment_due_date,
            expiration_date=self.expiration_date,
            education_years=self.education_years,
            last_downloaded_at=self.last_downloaded_at,
            is_archived=self.is_archived,
            file_id=FileIdVO(self.file_id),
            created_at=self.created_at,
            created_by=CreatedByVO(self.created_by),
            updated_at=self.updated_at,
            updated_by=UpdatedByVO(self.updated_by),
            deleted_at=self.deleted_at,
            deleted_by=DeletedByVO(self.updated_by),
        )
