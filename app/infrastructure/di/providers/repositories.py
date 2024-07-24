from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.faculty_students_counter import \
    IFacultyStudentsCounterRepository
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.protocols.repositories.uow import IUnitOfWork
from app.infrastructure.repositories.sqlalchemy_orm.contract_templates import \
    SqlalchemyContractTemplatesRepository
from app.infrastructure.repositories.sqlalchemy_orm.contracts import \
    SqlalchemyContractsRepository
from app.infrastructure.repositories.sqlalchemy_orm.faculty_contract_prices import \
    SqlalchemyFacultyContractPricesRepository
from app.infrastructure.repositories.sqlalchemy_orm.faculty_students_counter import \
    SqlalchemyFacultyStudentsCounterRepository
from app.infrastructure.repositories.sqlalchemy_orm.payments import \
    SqlalchemyPaymentsRepository
from app.infrastructure.repositories.sqlalchemy_orm.uow import \
    SqlalchemyUnitOfWork


class RepositoriesProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_uow_repository(self, session: FromDishka[AsyncSession]) -> IUnitOfWork:
        return SqlalchemyUnitOfWork(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_contract_templates_repository(
        self, session: FromDishka[AsyncSession]
    ) -> IContractTemplatesRepository:
        return SqlalchemyContractTemplatesRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_faculty_contract_prices_repository(
        self, session: FromDishka[AsyncSession]
    ) -> IFacultyContractPricesRepository:
        return SqlalchemyFacultyContractPricesRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_faculty_students_counter_repository(
        self, session: FromDishka[AsyncSession]
    ) -> IFacultyStudentsCounterRepository:
        return SqlalchemyFacultyStudentsCounterRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_contracts_repository(
        self, session: FromDishka[AsyncSession]
    ) -> IContractsRepository:
        return SqlalchemyContractsRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_payments_repository(
        self, session: FromDishka[AsyncSession]
    ) -> IPaymentsRepository:
        return SqlalchemyPaymentsRepository(session=session)
