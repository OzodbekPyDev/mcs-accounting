from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

from app.application.use_cases.contracts.create import CreateContract
from app.application.use_cases.contracts.get import (GetContractById,
                                                     GetListContracts,)
from app.application.use_cases.contracts.update import (
    UpdateContract, UpdateContractDownloadDetails,)
from app.domain.protocols.adapters.contract_number_provider import \
    ContractNumberProvider
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.docs_microservice_provider import \
    IDocsMicroserviceProvider
from app.domain.protocols.adapters.file_manager import FileManager
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.protocols.repositories.faculty_contract_prices import \
    IFacultyContractPricesRepository
from app.domain.protocols.repositories.faculty_students_counter import \
    IFacultyStudentsCounterRepository
from app.domain.protocols.repositories.uow import IUnitOfWork


class ContractsInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create(
        self,
        uow: FromDishka[IUnitOfWork],
        contracts_repository: FromDishka[IContractsRepository],
        contract_templates_repository: FromDishka[IContractTemplatesRepository],
        faculty_students_counter_repository: FromDishka[
            IFacultyStudentsCounterRepository
        ],
        faculty_contract_prices_repository: FromDishka[
            IFacultyContractPricesRepository
        ],
        id_provider: FromDishka[IdProvider],
        datetime_provider: FromDishka[DateTimeProvider],
        contract_number_provider: FromDishka[ContractNumberProvider],
        docs_microservice_provider: FromDishka[IDocsMicroserviceProvider],
        file_manager: FromDishka[FileManager],
    ) -> CreateContract:
        return CreateContract(
            uow=uow,
            contracts_repository=contracts_repository,
            contract_templates_repository=contract_templates_repository,
            faculty_students_counter_repository=faculty_students_counter_repository,
            faculty_contract_prices_repository=faculty_contract_prices_repository,
            id_provider=id_provider,
            datetime_provider=datetime_provider,
            contract_number_provider=contract_number_provider,
            docs_microservice_provider=docs_microservice_provider,
            file_manager=file_manager,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_all(
        self,
        contracts_repository: FromDishka[IContractsRepository],
    ) -> GetListContracts:
        return GetListContracts(
            contracts_repository=contracts_repository,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_by_id(
        self,
        contracts_repository: FromDishka[IContractsRepository],
    ) -> GetContractById:
        return GetContractById(contracts_repository=contracts_repository)

    @provide(scope=Scope.REQUEST)
    def provide_update(
        self,
        uow: FromDishka[IUnitOfWork],
        contracts_repository: FromDishka[IContractsRepository],
        datetime_provider: FromDishka[DateTimeProvider],
        docs_microservice_provider: FromDishka[IDocsMicroserviceProvider],
        file_manager: FromDishka[FileManager],
    ) -> UpdateContract:
        return UpdateContract(
            uow=uow,
            contracts_repository=contracts_repository,
            datetime_provider=datetime_provider,
            docs_microservice_provider=docs_microservice_provider,
            file_manager=file_manager,
        )

    @provide(scope=Scope.REQUEST)
    def provide_update_contract_download_details(
        self,
        uow: FromDishka[IUnitOfWork],
        contracts_repository: FromDishka[IContractsRepository],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> UpdateContractDownloadDetails:
        return UpdateContractDownloadDetails(
            uow=uow,
            contracts_repository=contracts_repository,
            datetime_provider=datetime_provider,
        )
