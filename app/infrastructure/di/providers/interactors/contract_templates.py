from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

from app.application.use_cases.contract_templates.create import \
    CreateContractTemplate
from app.application.use_cases.contract_templates.delete import \
    DeleteContractTemplate
from app.application.use_cases.contract_templates.get import (
    GetContractTemplateById, GetListContractTemplates,)
from app.application.use_cases.contract_templates.update import \
    UpdateContractTemplate
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.protocols.repositories.uow import IUnitOfWork


class ContractTemplatesInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create_interactor(
        self,
        uow: FromDishka[IUnitOfWork],
        contract_templates_repository: FromDishka[IContractTemplatesRepository],
        id_provider: FromDishka[IdProvider],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> CreateContractTemplate:
        return CreateContractTemplate(
            uow=uow,
            contract_templates_repository=contract_templates_repository,
            id_provider=id_provider,
            datetime_provider=datetime_provider,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_all_interactor(
        self,
        contract_templates_repository: FromDishka[IContractTemplatesRepository],
    ) -> GetListContractTemplates:
        return GetListContractTemplates(
            contract_templates_repository=contract_templates_repository,
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_by_id_interactor(
        self,
        contract_templates_repository: FromDishka[IContractTemplatesRepository],
    ) -> GetContractTemplateById:
        return GetContractTemplateById(
            contract_templates_repository=contract_templates_repository
        )

    @provide(scope=Scope.REQUEST)
    def provide_update_interactor(
        self,
        uow: FromDishka[IUnitOfWork],
        contract_templates_repository: FromDishka[IContractTemplatesRepository],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> UpdateContractTemplate:
        return UpdateContractTemplate(
            uow=uow,
            contract_templates_repository=contract_templates_repository,
            datetime_provider=datetime_provider,
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete_interactor(
        self,
        uow: FromDishka[IUnitOfWork],
        contract_templates_repository: FromDishka[IContractTemplatesRepository],
        datetime_provider: FromDishka[DateTimeProvider],
    ) -> DeleteContractTemplate:
        return DeleteContractTemplate(
            uow=uow,
            contract_templates_repository=contract_templates_repository,
            datetime_provider=datetime_provider,
        )
