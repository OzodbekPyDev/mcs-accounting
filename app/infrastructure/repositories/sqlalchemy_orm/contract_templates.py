from datetime import datetime

from asyncpg import UniqueViolationError
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.contract_templates import ContractTemplateEntity
from app.domain.entities.filter_params.contract_templates import \
    ContractTemplatesFilterParams
from app.domain.exceptions.constraints import UniqueConstraintsException
from app.domain.protocols.repositories.contract_templates import \
    IContractTemplatesRepository
from app.domain.value_objects.branch_id import BranchIdVO
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.id import IdVO
from app.infrastructure.db.models.sqlalchemy_orm.contract_templates import \
    ContractTemplate


class SqlalchemyContractTemplatesRepository(IContractTemplatesRepository):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ContractTemplateEntity) -> None:
        try:
            stmt = insert(ContractTemplate).values(
                id=data.id.value,
                branch_id=data.branch_id.value,
                degree_program=data.degree_program,
                language=data.language,
                info=data.info,
                name=data.name,
                html_content=data.html_content,
                is_active=data.is_active,
                start_date=data.start_date,
                first_payment_due_date=data.first_payment_due_date,
                expiration_date=data.expiration_date,
                education_years=data.education_years,
                created_by=data.created_by.value,
                created_at=data.created_at,
            )
            await self.session.execute(stmt)
        except UniqueViolationError:
            raise UniqueConstraintsException(
                "Contract template already exists. (UniqueViolationError)"
            )

    async def get_all(
        self, filter_params: ContractTemplatesFilterParams
    ) -> list[ContractTemplateEntity]:
        query = select(ContractTemplate)

        if not filter_params.with_deleted:
            query = query.filter(ContractTemplate.deleted_at.is_(None))

        if filter_params.branch_id:
            query = query.filter(
                ContractTemplate.branch_id == filter_params.branch_id.value
            )

        if filter_params.degree_program:
            query = query.filter(
                ContractTemplate.degree_program == filter_params.degree_program
            )

        if filter_params.language:
            query = query.filter(ContractTemplate.language == filter_params.language)

        if filter_params.is_active is not None:
            query = query.filter(
                ContractTemplate.is_active.is_(filter_params.is_active)
            )

        result = await self.session.execute(query)
        result = result.scalars().all()

        return [item.to_entity() for item in result]

    async def get_by_id(self, id: IdVO) -> ContractTemplateEntity | None:
        stmt = select(ContractTemplate).where(ContractTemplate.id == id.value)
        item = await self.session.execute(stmt)
        item = item.scalar_one_or_none()
        return item.to_entity() if item else None

    async def update(self, data: ContractTemplateEntity) -> None:
        stmt = (
            update(ContractTemplate)
            .where(ContractTemplate.id == data.id.value)
            .values(
                branch_id=data.branch_id.value,
                degree_program=data.degree_program,
                language=data.language,
                info=data.info,
                name=data.name,
                html_content=data.html_content,
                is_active=data.is_active,
                start_date=data.start_date,
                expiration_date=data.expiration_date,
                updated_by=data.updated_by.value,
                updated_at=data.updated_at,
            )
        )
        await self.session.execute(stmt)

    async def delete(
        self, id: IdVO, deleted_by: DeletedByVO, deleted_at: datetime
    ) -> None:
        stmt = (
            update(ContractTemplate)
            .where(
                ContractTemplate.id == id.value,
                ContractTemplate.deleted_at.is_(None),
            )
            .values(deleted_by=deleted_by.value, deleted_at=deleted_at)
        )
        await self.session.execute(stmt)

    async def get_appropriate_contract_template_or_none(
        self,
        branch_id: BranchIdVO,
        degree_program: str,
        language: str,
        current_datetime: datetime,
    ) -> ContractTemplateEntity | None:
        stmt = select(ContractTemplate).where(
            ContractTemplate.branch_id == branch_id.value,
            ContractTemplate.degree_program == degree_program,
            ContractTemplate.language == language,
            ContractTemplate.is_active.is_(True),
            ContractTemplate.start_date <= current_datetime,
            ContractTemplate.expiration_date > current_datetime,
            ContractTemplate.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()

        return item.to_entity() if item else None
