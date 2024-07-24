from typing import Protocol
from uuid import UUID


class IDocsMicroserviceProvider(Protocol):
    async def create_file(self, key: UUID, filename: str, content: bytes) -> None:
        raise NotImplementedError

    async def update_file(self, key: UUID, filename: str, content: bytes) -> None:
        raise NotImplementedError
