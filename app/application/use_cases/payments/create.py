from app.application.dto.payments import CreatePaymentRequest
from app.application.protocols.interactor import Interactor
from app.domain.entities.payments import PaymentEntity
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.exceptions.contracts import ContractNotFoundException
from app.domain.value_objects.id import IdVO
from app.domain.protocols.adapters.cabinet_mcs_provider import ICabinetMicroserviceProvider


class CreatePayment(Interactor[CreatePaymentRequest, None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        payments_repository: IPaymentsRepository,
        contracts_repository: IContractsRepository,
        cabinet_mcs_provider: ICabinetMicroserviceProvider,
        id_provider: IdProvider,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.payments_repository = payments_repository
        self.contracts_repository = contracts_repository
        self.cabinet_mcs_provider = cabinet_mcs_provider
        self.id_provider = id_provider
        self.datetime_provider = datetime_provider

    async def __call__(self, request: CreatePaymentRequest) -> None:
        """CHECK IF CONTRACT NUMBER EXISTS"""
        # contract_exists = await self.contracts_repository.is_contract_number_exists(
        #     contract_number=request.contract_number
        # )
        # if not contract_exists:
        #     raise ContractNotFoundException("Contract not found, incorrect contract number")
        #
        # """CHECK IF PASSPORT NUMBER EXISTS"""
        # passport_exists = await self.cabinet_mcs_provider.is_passport_number_exists(
        #     passport_number=request.passport_number
        # )
        #
        # if not passport_exists:
        #     raise ContractNotFoundException("Incorrect passport number")

        payment_entity = await self.payments_repository.get_by_contract_number(contract_number=request.contract_number)
        """IF PAYMENT EXISTS THEN UPDATE PAYMENT"""
        if payment_entity:
            payment_entity.update(
                full_name=request.full_name,
                pinfl=request.pinfl,
                amount=request.amount,
                updated_at=self.datetime_provider.get_current_time(),
            )
            await self.payments_repository.update(payment_entity)
        else:
            """IF PAYMENT DOES NOT EXISTS THEN CREATE NEW PAYMENT"""
            payment_entity = PaymentEntity(
                id=IdVO(value=self.id_provider.generate_uuid()),
                created_at=self.datetime_provider.get_current_time(),
                updated_at=None,
                deleted_at=None,
                contract_number=request.contract_number,
                full_name=request.full_name,
                passport_number=request.passport_number,
                pinfl=request.pinfl,
                amount=request.amount,
            )
            await self.payments_repository.create(payment_entity)
        await self.uow.commit()
