from typing import Protocol
from uuid import UUID


class ICabinetMicroserviceProvider(Protocol):
    async def is_passport_number_exists(self, passport_number: str) -> bool:
        raise NotImplementedError


