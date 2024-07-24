from app.application.dto.faculty_contract_prices import (
    CreateFacultyContractPriceRequest, FacultyContractPriceResponse,)
from app.application.protocols.interactor import Interactor
from app.domain.entities.faculty_contract_prices import \
    FacultyContractPriceEntity
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)
from app.domain.value_objects.faculty_id import FacultyIdVO
from app.domain.value_objects.id import IdVO


class CreateFacultyContractPrice(
    Interactor[CreateFacultyContractPriceRequest, FacultyContractPriceResponse]
):

    def __init__(
        self,
        uow: IUnitOfWork,
        faculty_contract_prices_repository: IFacultyContractPricesRepository,
        id_provider: IdProvider,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.faculty_contract_prices_repository = faculty_contract_prices_repository
        self.id_provider = id_provider
        self.datetime_provider = datetime_provider

    async def __call__(
        self, request: CreateFacultyContractPriceRequest
    ) -> FacultyContractPriceResponse:
        fac_con_price_entity = FacultyContractPriceEntity(
            id=IdVO(value=self.id_provider.generate_uuid()),
            faculty_id=FacultyIdVO(value=request.faculty_id),
            amount=request.amount,
            transcriptions=request.transcriptions,
            created_at=self.datetime_provider.get_current_time(),
            updated_at=None,
            deleted_at=None,
            created_by=CreatedByVO(value=request.created_by),
            updated_by=UpdatedByVO(value=None),
            deleted_by=DeletedByVO(value=None),
        )
        await self.faculty_contract_prices_repository.create(fac_con_price_entity)
        await self.uow.commit()
        return FacultyContractPriceResponse.from_entity(fac_con_price_entity)
