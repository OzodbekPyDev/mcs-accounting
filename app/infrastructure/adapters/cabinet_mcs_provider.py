from app.domain.protocols.adapters.cabinet_mcs_provider import ICabinetMicroserviceProvider
from app.infrastructure.config import settings
import httpx


class CabinetMicroserviceProvider(ICabinetMicroserviceProvider):

    async def is_passport_number_exists(
        self,
        passport_number: str,
    ) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.CABINET_MCS_URL}{passport_number}"
            )
            return response.status_code == 200

