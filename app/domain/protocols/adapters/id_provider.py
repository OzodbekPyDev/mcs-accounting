from typing import Protocol
from uuid import UUID


class IdProvider(Protocol):
    def generate_uuid(self) -> UUID:
        raise NotImplementedError

    def generate_uuid_v6(self) -> UUID:
        raise NotImplementedError
