from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity
from app.domain.entities.mixins.admin_mixin import AdminMixinEntity
from app.domain.value_objects.created_updated_by import UpdatedByVO
from app.domain.value_objects.faculty_id import FacultyIdVO


@dataclass
class FacultyContractPriceEntity(BaseEntity, AdminMixinEntity):
    faculty_id: FacultyIdVO
    amount: int
    transcriptions: dict[str, str]

    def update(
        self,
        faculty_id: FacultyIdVO,
        amount: int,
        transcriptions: dict[str, str],
        updated_at: datetime,
        updated_by: UpdatedByVO,
    ) -> None:
        self.faculty_id = faculty_id
        self.amount = amount
        self.transcriptions = transcriptions
        self.updated_at = updated_at
        self.updated_by = updated_by
