from datetime import datetime
from typing import Protocol
from app.domain.entities.payments import PaymentEntity


class IService1CProvider(Protocol):
    async def get_payments(self) -> list[PaymentEntity]:
        raise NotImplementedError
