from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, unique=True)

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime | None]

    deleted_at: Mapped[datetime | None]
