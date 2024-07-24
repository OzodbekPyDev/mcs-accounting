from datetime import datetime
from typing import Protocol

from app.domain.entities.faculty_contract_prices import \
    FacultyContractPriceEntity
from app.domain.entities.filter_params.faculty_contract_prices import \
    FacultyContractPricesFilterParams
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO


class IFacultyContractPricesRepository(Protocol):
    async def create(self, data: FacultyContractPriceEntity) -> None:
        raise NotImplementedError

    async def get_all(
        self, filter_params: FacultyContractPricesFilterParams
    ) -> list[FacultyContractPriceEntity]:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> FacultyContractPriceEntity | None:
        raise NotImplementedError

    async def update(self, data: FacultyContractPriceEntity) -> None:
        raise NotImplementedError

    async def delete(
        self, id: IdVO, deleted_by: DeletedByVO, deleted_at: datetime
    ) -> None:
        raise NotImplementedError

    async def get_by_faculty_id(
        self, faculty_id: FacultyIdVO
    ) -> FacultyContractPriceEntity | None:
        raise NotImplementedError
