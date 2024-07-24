from app.application.dto.faculty_contract_prices import (
    FacultyContractPriceResponse, UpdateFacultyContractPriceRequest,)
from app.application.protocols.interactor import Interactor
from app.domain.exceptions.faculty_contract_prices import \
    FacultyContractPriceNotFoundException
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.created_updated_by import UpdatedByVO
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO


class UpdateFacultyContractPrice(
    Interactor[UpdateFacultyContractPriceRequest, FacultyContractPriceResponse]
):

    def __init__(
        self,
        uow: IUnitOfWork,
        faculty_contract_prices_repository: IFacultyContractPricesRepository,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.faculty_contract_prices_repository = faculty_contract_prices_repository
        self.datetime_provider = datetime_provider

    async def __call__(
        self, request: UpdateFacultyContractPriceRequest
    ) -> FacultyContractPriceResponse:
        fac_con_price_entity = await self.faculty_contract_prices_repository.get_by_id(
            id=IdVO(value=request.id)
        )
        if not fac_con_price_entity:
            raise FacultyContractPriceNotFoundException(
                "Faculty contract price not found"
            )

        fac_con_price_entity.update(
            faculty_id=FacultyIdVO(value=request.faculty_id),
            amount=request.amount,
            transcriptions=request.transcriptions,
            updated_at=self.datetime_provider.get_current_time(),
            updated_by=UpdatedByVO(value=request.updated_by),
        )

        await self.faculty_contract_prices_repository.update(fac_con_price_entity)
        await self.uow.commit()
        return FacultyContractPriceResponse.from_entity(fac_con_price_entity)
