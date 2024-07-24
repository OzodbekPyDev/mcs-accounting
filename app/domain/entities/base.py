from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.id import IdVO


@dataclass
class BaseEntity:
    id: IdVO

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None
