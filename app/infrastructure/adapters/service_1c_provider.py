from app.domain.protocols.adapters.service_1c_provider import IService1CProvider
from app.domain.entities.payments import PaymentEntity
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.value_objects.id import IdVO


class Service1CProvider(IService1CProvider):

    def __init__(
            self,
            id_provider: IdProvider,
            datetime_provider: DateTimeProvider,
    ) -> None:
        self.id_provider = id_provider
        self.datetime_provider = datetime_provider

    async def get_payments(self) -> list[PaymentEntity]:
        response = [
            {
                "contract_number": "2022/IT-01-001/1",
                "full_name": "John Doe",
                "passport_number": "AA1234567",
                "pinfl": "12345678901234",
                "amount": 100.0,
            }
        ]

        current_datetime = self.datetime_provider.get_current_time()

        return [
            PaymentEntity(
                id=IdVO(value=self.id_provider.generate_uuid()),
                created_at=current_datetime,
                updated_at=None,
                deleted_at=None,
                contract_number=data["contract_number"],
                full_name=data["full_name"],
                passport_number=data["passport_number"],
                pinfl=data["pinfl"],
                amount=data["amount"],
            )
            for data in response
        ]
