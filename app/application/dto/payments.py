from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.payments import PaymentEntity, PaymentStatus


@dataclass
class CreatePaymentRequest:
    contract_number: str
    full_name: str | None
    passport_number: str
    pinfl: str | None
    amount: float


@dataclass
class UpdatePaymentRequest:
    id: UUID
    contract_number: str
    full_name: str | None
    passport_number: str
    pinfl: str | None
    amount: float


@dataclass
class PaymentResponse:
    id: UUID
    contract_number: str
    full_name: str | None
    passport_number: str
    pinfl: str | None
    status: PaymentStatus
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: PaymentEntity) -> "PaymentResponse":
        return cls(
            id=entity.id.value,
            contract_number=entity.contract_number,
            full_name=entity.full_name,
            passport_number=entity.passport_number,
            pinfl=entity.pinfl,
            status=entity.status,
            created_at=entity.created_at,
        )


@dataclass
class SynchronizationPaymentsResponse:
    qty_success_payments: int
    qty_failed_payments: int
    failed_payments: list[PaymentResponse]


@dataclass
class GetListPaymentsRequest:
    passport_number: str | None = None
    contract_number: str | None = None
    pinfl: str | None = None
