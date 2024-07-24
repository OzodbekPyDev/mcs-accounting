from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

from app.application.use_cases.faculty_contract_prices.create import \
    CreateFacultyContractPrice
from app.application.use_cases.faculty_contract_prices.delete import \
    DeleteFacultyContractPrice
from app.application.use_cases.faculty_contract_prices.get import (
    GetFacultyContractPriceById, GetListFacultyContractPrices,)
from app.application.use_cases.faculty_contract_prices.update import \
    UpdateFacultyContractPrice
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork


class FacultyContractPricesInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create(
        self,
        uow: FromDishka[IUnitOfWork],
        faculty_contract_prices_repository: FromDishka[
            IFacultyContractPricesRepository
        ],
        id_provider: FromDishka[IdProvider],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> CreateFacultyContractPrice:
        return CreateFacultyContractPrice(
            uow=uow,
            faculty_contract_prices_repository=faculty_contract_prices_repository,
            id_provider=id_provider,
            datetime_provider=datetime_provider,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_all(
        self,
        faculty_contract_prices_repository: FromDishka[
            IFacultyContractPricesRepository
        ],
    ) -> GetListFacultyContractPrices:
        return GetListFacultyContractPrices(
            faculty_contract_prices_repository=faculty_contract_prices_repository,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_by_id(
        self,
        faculty_contract_prices_repository: FromDishka[
            IFacultyContractPricesRepository
        ],
    ) -> GetFacultyContractPriceById:
        return GetFacultyContractPriceById(
            faculty_contract_prices_repository=faculty_contract_prices_repository,
        )

    @provide(scope=Scope.REQUEST)
    def update(
        self,
        uow: FromDishka[IUnitOfWork],
        faculty_contract_prices_repository: FromDishka[
            IFacultyContractPricesRepository
        ],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> UpdateFacultyContractPrice:
        return UpdateFacultyContractPrice(
            uow=uow,
            faculty_contract_prices_repository=faculty_contract_prices_repository,
            datetime_provider=datetime_provider,
        )

    @provide(scope=Scope.REQUEST)
    def delete(
        self,
        uow: FromDishka[IUnitOfWork],
        faculty_contract_prices_repository: FromDishka[
            IFacultyContractPricesRepository
        ],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> DeleteFacultyContractPrice:
        return DeleteFacultyContractPrice(
            uow=uow,
            faculty_contract_prices_repository=faculty_contract_prices_repository,
            datetime_provider=datetime_provider,
        )
