from uuid import UUID

from sqlalchemy import JSON, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.entities.faculty_contract_prices import \
    FacultyContractPriceEntity
from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm import Base
from app.infrastructure.db.models.sqlalchemy_orm.mixins.admin_mixin import \
    AdminMixin


class FacultyContractPrice(Base, AdminMixin):
    __tablename__ = "faculty_contract_prices"
    __table_args__ = (
        Index(
            "ix_unique_active_faculty_id",
            "faculty_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    faculty_id: Mapped[UUID]
    amount: Mapped[int]
    transcriptions: Mapped[dict] = mapped_column(type_=JSON)

    def to_entity(self) -> FacultyContractPriceEntity:
        return FacultyContractPriceEntity(
            id=IdVO(self.id),
            faculty_id=FacultyIdVO(self.faculty_id),
            amount=self.amount,
            transcriptions=self.transcriptions,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
            created_by=CreatedByVO(self.created_by),
            updated_by=UpdatedByVO(self.updated_by),
            deleted_by=DeletedByVO(self.deleted_by),
        )
