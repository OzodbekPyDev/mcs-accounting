from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

from app.application.use_cases.payments.create import CreatePayment
from app.application.use_cases.payments.delete import DeleteAllPayments
from app.application.use_cases.payments.get import (GetListPayments,
                                                    GetPaymentById,)
from app.application.use_cases.payments.synchronize_data import \
    SynchronizePaymentsData
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.domain.protocols.adapters.cabinet_mcs_provider import ICabinetMicroserviceProvider
from app.domain.protocols.adapters.service_1c_provider import IService1CProvider


class PaymentsInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create(
        self,
        uow: FromDishka[IUnitOfWork],
        payments_repository: FromDishka[IPaymentsRepository],
        contracts_repository: FromDishka[IContractsRepository],
        cabinet_mcs_provider: FromDishka[ICabinetMicroserviceProvider],
        id_provider: FromDishka[IdProvider],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> CreatePayment:
        return CreatePayment(
            uow=uow,
            payments_repository=payments_repository,
            contracts_repository=contracts_repository,
            cabinet_mcs_provider=cabinet_mcs_provider,
            id_provider=id_provider,
            datetime_provider=datetime_provider,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_all(
        self,
        payments_repository: FromDishka[IPaymentsRepository],
    ) -> GetListPayments:
        return GetListPayments(
            payments_repository=payments_repository,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_by_id(
        self,
        payments_repository: FromDishka[IPaymentsRepository],
    ) -> GetPaymentById:
        return GetPaymentById(
            payments_repository=payments_repository,
        )

    @provide(scope=Scope.REQUEST)
    def provide_synchronize_data(
        self,
        uow: FromDishka[IUnitOfWork],
        payments_repository: FromDishka[IPaymentsRepository],
        contracts_repository: FromDishka[IContractsRepository],
        id_provider: FromDishka[IdProvider],
        datetime_provider: FromDishka[DateTimeProvider],
        service_1c_provider: FromDishka[IService1CProvider],
        cabinet_mcs_provider: FromDishka[ICabinetMicroserviceProvider],
    ) -> SynchronizePaymentsData:
        return SynchronizePaymentsData(
            uow=uow,
            payments_repository=payments_repository,
            contracts_repository=contracts_repository,
            id_provider=id_provider,
            datetime_provider=datetime_provider,
            service_1c_provider=service_1c_provider,
            cabinet_mcs_provider=cabinet_mcs_provider,
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete_all(
        self,
        uow: FromDishka[IUnitOfWork],
        payments_repository: FromDishka[IPaymentsRepository],
    ) -> DeleteAllPayments:
        return DeleteAllPayments(
            uow=uow,
            payments_repository=payments_repository,
        )
