from app.application.protocols.interactor import Interactor
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.adapters.service_1c_provider import IService1CProvider
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.application.dto.payments import SynchronizationPaymentsResponse, PaymentResponse
from app.domain.protocols.adapters.cabinet_mcs_provider import ICabinetMicroserviceProvider


class SynchronizePaymentsData(Interactor[None, SynchronizationPaymentsResponse]):

    def __init__(
        self,
        uow: IUnitOfWork,
        payments_repository: IPaymentsRepository,
        contracts_repository: IContractsRepository,
        service_1c_provider: IService1CProvider,
        cabinet_mcs_provider: ICabinetMicroserviceProvider,
        id_provider: IdProvider,
        datetime_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.payments_repository = payments_repository
        self.contracts_repository = contracts_repository
        self.id_provider = id_provider
        self.datetime_provider = datetime_provider
        self.service_1c_provider = service_1c_provider
        self.cabinet_mcs_provider = cabinet_mcs_provider

    async def __call__(self, request: None) -> SynchronizationPaymentsResponse:
        """DELETE ALL PAYMENTS DATA FROM DATABASE
           IN ORDER TO SYNCHRONIZE IT WITH EXTERNAL API DATA"""
        await self.payments_repository.delete_all()
        """ADAPTER TO GET ALL DATA FROM EXTERNAL API AND SYNCHRONIZE IT WITH DATABASE"""
        payment_entities = await self.service_1c_provider.get_payments()

        success_payments = []
        failed_payments = []

        for payment in payment_entities:
            """CHECK IF THE CONTRACT NUMBER AND PASSPORT NUMBER EXIST IN DATABASE"""
            contract_exists = await self.contracts_repository.is_contract_number_exists(
                contract_number=payment.contract_number
            )

            passport_exists = await self.cabinet_mcs_provider.is_passport_number_exists(
                passport_number=payment.passport_number
            )

            if not contract_exists or not passport_exists:
                failed_payments.append(payment)
                continue
                # Переход к следующей итерации цикла, то есть этот платеж не будет добавлен в success_payments

            success_payments.append(payment)

        if success_payments:
            await self.payments_repository.bulk_create(success_payments)

            await self.uow.commit()

        return SynchronizationPaymentsResponse(
            qty_success_payments=len(success_payments),
            qty_failed_payments=len(failed_payments),
            failed_payments=[
                PaymentResponse.from_entity(payment)
                for payment in failed_payments
            ]
        )



