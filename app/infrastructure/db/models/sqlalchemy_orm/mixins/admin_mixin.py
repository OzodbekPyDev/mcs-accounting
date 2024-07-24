from uuid import UUID

from sqlalchemy.orm import Mapped


class AdminMixin:
    created_by: Mapped[UUID]
    updated_by: Mapped[UUID | None]
    deleted_by: Mapped[UUID | None]
