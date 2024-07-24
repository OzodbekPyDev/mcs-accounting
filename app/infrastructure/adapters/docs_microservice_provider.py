from uuid import UUID

import httpx

from app.domain.exceptions.pdf_generation import \
    FileCouldNotBeSavedInDocsException
from app.domain.protocols.adapters.docs_microservice_provider import \
    IDocsMicroserviceProvider
from app.infrastructure.config import settings


class DocsMicroserviceProvider(IDocsMicroserviceProvider):

    async def create_file(self, key: UUID, filename: str, content: bytes) -> None:
        data = {"key": str(key)}
        files = {"file": (filename, content)}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.DOCS_MCS_URL, data=data, files=files
                )
                if response.status_code != 201:
                    raise FileCouldNotBeSavedInDocsException(
                        "Failed to save file in DOCS MCS"
                    )
        except Exception:
            raise FileCouldNotBeSavedInDocsException(
                "Could not connect to the DOCS MCS"
            )

    async def update_file(self, key: UUID, filename: str, content: bytes) -> None:
        files = {"file": (filename, content)}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{settings.DOCS_MCS_URL}{key}", files=files
                )
                if response.status_code != 200:
                    raise FileCouldNotBeSavedInDocsException(
                        "Failed to update file in DOCS MCS"
                    )
        except Exception:
            raise FileCouldNotBeSavedInDocsException(
                "Could not connect to the DOCS MCS"
            )
