from typing import Protocol

from app.domain.entities.payments import PaymentEntity
from app.domain.value_objects.id import IdVO

from app.domain.entities.filter_params.payments import PaymentsFilterParams


class IPaymentsRepository(Protocol):

    async def bulk_create(self, entities: list[PaymentEntity]) -> None:
        raise NotImplementedError

    async def create(self, entity: PaymentEntity) -> None:
        raise NotImplementedError

    async def get_all(self, filter_params: PaymentsFilterParams) -> list[PaymentEntity]:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> PaymentEntity | None:
        raise NotImplementedError

    async def get_by_contract_number(
        self, contract_number: str
    ) -> PaymentEntity | None:
        raise NotImplementedError

    async def update(self, entity: PaymentEntity) -> None:
        raise NotImplementedError

    async def delete_all(self) -> None:
        raise NotImplementedError
