from uuid import UUID

from app.application.dto.contracts import (ContractResponse,
                                           GetListContractsRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.entities.filter_params.contracts import ContractsFilterParams
from app.domain.exceptions.contracts import ContractNotFoundException
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.value_objects.id import IdVO
from app.domain.value_objects.student_id import StudentIdVO


class GetListContracts(Interactor[GetListContractsRequest, list[ContractResponse]]):

    def __init__(
        self,
        contracts_repository: IContractsRepository,
    ) -> None:
        self.contracts_repository = contracts_repository

    async def __call__(
        self, request: GetListContractsRequest
    ) -> list[ContractResponse]:

        contracts = await self.contracts_repository.get_all(
            ContractsFilterParams(
                student_id=(
                    StudentIdVO(value=request.student_id)
                    if request.student_id
                    else None
                ),
                html_content=request.html_content,
                with_deleted=request.with_deleted,
            )
        )
        return [ContractResponse.from_entity(contract) for contract in contracts]


class GetContractById(Interactor[UUID, ContractResponse]):

    def __init__(
        self,
        contracts_repository: IContractsRepository,
    ) -> None:
        self.contracts_repository = contracts_repository

    async def __call__(self, request: UUID) -> ContractResponse:
        contract = await self.contracts_repository.get_by_id(IdVO(value=request))
        if not contract:
            raise ContractNotFoundException("Contract not found.")
        return ContractResponse.from_entity(contract)
