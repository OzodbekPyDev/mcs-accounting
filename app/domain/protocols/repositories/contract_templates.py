from datetime import datetime
from typing import Protocol

from app.domain.entities.contract_templates import ContractTemplateEntity
from app.domain.entities.filter_params.contract_templates import \
    ContractTemplatesFilterParams
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.id import IdVO


class IContractTemplatesRepository(Protocol):
    async def create(self, data: ContractTemplateEntity) -> None:
        raise NotImplementedError

    async def get_all(
        self, filter_params: ContractTemplatesFilterParams
    ) -> list[ContractTemplateEntity]:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> ContractTemplateEntity | None:
        raise NotImplementedError

    async def update(self, data: ContractTemplateEntity) -> None:
        raise NotImplementedError

    async def delete(
        self, id: IdVO, deleted_by: DeletedByVO, deleted_at: datetime
    ) -> None:
        raise NotImplementedError

    async def get_appropriate_contract_template_or_none(
        self,
        branch_id: BranchIdVO,
        degree_program: str,
        language: str,
        current_datetime: datetime,
    ) -> ContractTemplateEntity | None:
        raise NotImplementedError
