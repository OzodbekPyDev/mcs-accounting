from uuid import UUID, uuid4

from uuid6 import uuid6

from app.domain.protocols.adapters import IdProvider


class SystemIdProvider(IdProvider):
    def generate_uuid(self) -> UUID:
        return uuid4()

    def generate_uuid_v6(self) -> UUID:
        return uuid6()
