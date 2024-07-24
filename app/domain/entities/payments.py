from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity

from enum import Enum


class PaymentStatus(str, Enum):
    prepayment = "prepayment"
    paid = "paid"
    debt = "debt"
    error = "error"


@dataclass
class PaymentEntity(BaseEntity):
    contract_number: str
    full_name: str | None
    passport_number: str
    pinfl: str | None
    amount: float

    @property
    def status(self) -> PaymentStatus:
        if self.amount == 0:
            return PaymentStatus.paid
        elif self.amount > 0:
            return PaymentStatus.prepayment
        elif self.amount < 0:
            return PaymentStatus.debt
        else:
            return PaymentStatus.error

    def update(
        self,
        full_name: str | None,
        pinfl: str | None,
        amount: float,
        updated_at: datetime,
    ) -> None:
        self.full_name = full_name
        self.pinfl = pinfl
        self.amount = amount
        self.updated_at = updated_at


