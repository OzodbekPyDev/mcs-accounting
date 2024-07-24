from datetime import datetime
from typing import Protocol

from app.domain.entities.contracts import (ContractDownloadEntity,
                                           ContractEntity,)
from app.domain.entities.filter_params.contracts import ContractsFilterParams
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.id import IdVO
from app.domain.value_objects.student_id import StudentIdVO


class IContractsRepository(Protocol):
    async def create(self, data: ContractEntity) -> None:
        raise NotImplementedError

    async def get_all(
        self, filter_params: ContractsFilterParams
    ) -> list[ContractEntity]:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> ContractEntity | None:
        raise NotImplementedError

    async def get_student_active_contract_key_details_to_download(
        self,
        id: IdVO,
        current_datetime: datetime,
    ) -> ContractDownloadEntity | None:
        raise NotImplementedError

    async def update(self, data: ContractEntity) -> None:
        raise NotImplementedError

    async def delete(
        self, id: IdVO, deleted_by: DeletedByVO, deleted_at: datetime
    ) -> None:
        raise NotImplementedError

    async def has_contract_in_current_education_year(
        self, student_id: StudentIdVO, current_datetime: datetime
    ) -> bool:
        raise NotImplementedError

    async def update_contract_download_details(
        self, id: IdVO, download_counter: int, last_downloaded_at: datetime
    ) -> None:
        raise NotImplementedError

    async def is_contract_number_exists(self, contract_number: str) -> bool:
        raise NotImplementedError
