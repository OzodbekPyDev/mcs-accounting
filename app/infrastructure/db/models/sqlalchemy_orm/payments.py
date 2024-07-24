from sqlalchemy.orm import Mapped
from sqlalchemy import Index, text

from app.domain.entities.payments import PaymentEntity
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        Index(
            "ix_unique_contract_number_passport_number",
            "contract_number",
            "passport_number",
            unique=True,
        ),
    )

    contract_number: Mapped[str]
    full_name: Mapped[str | None]
    passport_number: Mapped[str]
    pinfl: Mapped[str | None]
    amount: Mapped[float]

    def to_entity(self) -> PaymentEntity:
        return PaymentEntity(
            id=IdVO(self.id),
            contract_number=self.contract_number,
            full_name=self.full_name,
            passport_number=self.passport_number,
            pinfl=self.pinfl,
            amount=self.amount,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )
