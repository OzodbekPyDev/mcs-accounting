from uuid import UUID

from app.application.dto.faculty_contract_prices import (
    FacultyContractPriceResponse, GetAllFacultyContractPricesRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.entities.filter_params.faculty_contract_prices import \
    FacultyContractPricesFilterParams
from app.domain.exceptions.faculty_contract_prices import \
    FacultyContractPriceNotFoundException
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.value_objects.id import IdVO


class GetListFacultyContractPrices(
    Interactor[GetAllFacultyContractPricesRequest, list[FacultyContractPriceResponse]]
):

    def __init__(
        self,
        faculty_contract_prices_repository: IFacultyContractPricesRepository,
    ) -> None:
        self.faculty_contract_prices_repository = faculty_contract_prices_repository

    async def __call__(
        self, request: GetAllFacultyContractPricesRequest
    ) -> list[FacultyContractPriceResponse]:
        faculty_contract_prices_entities = (
            await self.faculty_contract_prices_repository.get_all(
                filter_params=FacultyContractPricesFilterParams(
                    with_deleted=request.with_deleted
                )
            )
        )
        return [
            FacultyContractPriceResponse.from_entity(entity)
            for entity in faculty_contract_prices_entities
        ]


class GetFacultyContractPriceById(Interactor[UUID, FacultyContractPriceResponse]):

    def __init__(
        self,
        faculty_contract_prices_repository: IFacultyContractPricesRepository,
    ) -> None:
        self.faculty_contract_prices_repository = faculty_contract_prices_repository

    async def __call__(self, request: UUID) -> FacultyContractPriceResponse:
        faculty_contract_price_entity = (
            await self.faculty_contract_prices_repository.get_by_id(
                id=IdVO(value=request)
            )
        )
        if not faculty_contract_price_entity:
            raise FacultyContractPriceNotFoundException(
                "Faculty contract price not found"
            )
        return FacultyContractPriceResponse.from_entity(faculty_contract_price_entity)
