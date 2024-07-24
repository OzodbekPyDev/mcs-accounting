from uuid import UUID

from app.application.dto.contract_templates import (
    ContractTemplateResponse, GetListContractTemplatesRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.entities.filter_params.contract_templates import \
    ContractTemplatesFilterParams
from app.domain.exceptions.contract_templates import \
    ContractTemplateNotFoundException
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.id import IdVO


class GetListContractTemplates(
    Interactor[GetListContractTemplatesRequest, list[ContractTemplateResponse]]
):

    def __init__(
        self,
        contract_templates_repository: IContractTemplatesRepository,
    ) -> None:
        self.contract_templates_repository = contract_templates_repository

    async def __call__(
        self, request: GetListContractTemplatesRequest
    ) -> list[ContractTemplateResponse]:
        cont_temp_entities = await self.contract_templates_repository.get_all(
            filter_params=ContractTemplatesFilterParams(
                with_deleted=request.with_deleted,
                branch_id=(
                    BranchIdVO(value=request.branch_id) if request.branch_id else None
                ),
                degree_program=request.degree_program,
                language=request.language,
                is_active=request.is_active,
            )
        )
        return [
            ContractTemplateResponse.from_entity(entity)
            for entity in cont_temp_entities
        ]


class GetContractTemplateById(Interactor[UUID, ContractTemplateResponse]):

    def __init__(
        self,
        contract_templates_repository: IContractTemplatesRepository,
    ) -> None:
        self.contract_templates_repository = contract_templates_repository

    async def __call__(self, request: UUID) -> ContractTemplateResponse:
        cont_temp_entity = await self.contract_templates_repository.get_by_id(
            id=IdVO(value=request)
        )
        if not cont_temp_entity:
            raise ContractTemplateNotFoundException("Contract template not found")
        return ContractTemplateResponse.from_entity(cont_temp_entity)
