from dishka import Provider, Scope, provide

from app.domain.protocols.adapters.contract_number_provider import \
    ContractNumberProvider
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.docs_microservice_provider import \
    IDocsMicroserviceProvider
from app.domain.protocols.adapters.file_manager import FileManager
from app.domain.protocols.adapters.id_provider import IdProvider
from app.infrastructure.adapters.contract_number_provider import \
    SystemContractNumberProvider
from app.infrastructure.adapters.datetime_provider import (
    SystemDateTimeProvider, Timezone,)
from app.infrastructure.adapters.docs_microservice_provider import \
    DocsMicroserviceProvider
from app.infrastructure.adapters.file_manager import JinjaPdfkitFileManager
from app.infrastructure.adapters.id_provider import SystemIdProvider
from app.domain.protocols.adapters.service_1c_provider import IService1CProvider
from app.infrastructure.adapters.service_1c_provider import Service1CProvider
from app.domain.protocols.adapters.cabinet_mcs_provider import ICabinetMicroserviceProvider
from app.infrastructure.adapters.cabinet_mcs_provider import CabinetMicroserviceProvider


class AdaptersProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_date_time_provider(self) -> DateTimeProvider:
        return SystemDateTimeProvider(Timezone.UTC)

    @provide(scope=Scope.APP)
    def provide_id_provider(self) -> IdProvider:
        return SystemIdProvider()

    @provide(scope=Scope.APP)
    def provide_contract_number_provider(
        self,
    ) -> ContractNumberProvider:
        return SystemContractNumberProvider()

    @provide(scope=Scope.APP)
    def provide_docs_microservice_provider(self) -> IDocsMicroserviceProvider:
        return DocsMicroserviceProvider()

    @provide(scope=Scope.APP)
    def provide_file_manager(self) -> FileManager:
        return JinjaPdfkitFileManager()

    @provide(scope=Scope.APP)
    def provide_service_1c_provider(
            self,
            id_provider: IdProvider,
            datetime_provider: DateTimeProvider,
    ) -> IService1CProvider:
        return Service1CProvider(
            id_provider=id_provider,
            datetime_provider=datetime_provider,
        )

    @provide(scope=Scope.APP)
    def provide_cabinet_mcs_provider(self) -> ICabinetMicroserviceProvider:
        return CabinetMicroserviceProvider()
