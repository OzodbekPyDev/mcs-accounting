from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class FileIdVO:
    value: UUID
