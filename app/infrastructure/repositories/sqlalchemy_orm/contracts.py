from datetime import datetime

from sqlalchemy import and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.entities.contracts import (ContractDownloadEntity,
                                           ContractEntity,)
from app.domain.entities.filter_params.contracts import ContractsFilterParams
from app.domain.protocols.repositories.contracts import IContractsRepository
from app.domain.value_objects.created_updated_by import DeletedByVO
from app.domain.value_objects.file_id import FileIdVO
from app.domain.value_objects.id import IdVO
from app.domain.value_objects.student_id import StudentIdVO
from app.infrastructure.db.models.sqlalchemy_orm.contracts import Contract


class SqlalchemyContractsRepository(IContractsRepository):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ContractEntity) -> None:
        stmt = insert(Contract).values(
            id=data.id.value,
            student_id=data.student_id.value,
            template_id=data.template_id.value,
            html_content=data.html_content,
            number=data.number,
            download_counter=data.download_counter,
            start_date=data.start_date,
            first_payment_due_date=data.first_payment_due_date,
            expiration_date=data.expiration_date,
            education_years=data.education_years,
            last_downloaded_at=data.last_downloaded_at,
            is_archived=data.is_archived,
            file_id=data.file_id.value,
            created_at=data.created_at,
            created_by=data.created_by.value,
        )
        await self.session.execute(stmt)

    async def get_all(
        self, filter_params: ContractsFilterParams
    ) -> list[ContractEntity]:
        query = select(Contract).options(joinedload(Contract.template))

        if not filter_params.with_deleted:
            query = query.where(Contract.deleted_at.is_(None))

        if filter_params.student_id:
            query = query.where(Contract.student_id == filter_params.student_id.value)

        if filter_params.html_content:
            query = query.where(Contract.html_content == filter_params.html_content)

        result = await self.session.execute(query)
        result = result.scalars().all()
        return [item.to_entity() for item in result]

    async def get_by_id(self, id: IdVO) -> ContractEntity | None:
        stmt = (
            select(Contract)
            .options(joinedload(Contract.template))
            .where(Contract.id == id.value)
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_entity() if item else None

    async def get_student_active_contract_key_details_to_download(
        self,
        id: IdVO,
        current_datetime: datetime,
    ) -> ContractDownloadEntity | None:
        stmt = select(
            Contract.id,
            Contract.student_id,
            Contract.file_id,
            Contract.download_counter,
            Contract.last_downloaded_at,
        ).where(
            Contract.id == id.value,
            Contract.start_date <= current_datetime,
            Contract.expiration_date > current_datetime,
            Contract.is_archived.is_(False),
        )
        result = await self.session.execute(stmt)
        item = result.one_or_none()
        return (
            ContractDownloadEntity(
                id=IdVO(item.id),
                student_id=StudentIdVO(item.student_id),
                file_id=FileIdVO(item.file_id),
                download_counter=item.download_counter,
                last_downloaded_at=item.last_downloaded_at,
            )
            if item
            else None
        )

    async def update(self, data: ContractEntity) -> None:
        stmt = (
            update(Contract)
            .where(Contract.id == data.id.value)
            .values(
                template_id=data.template_id.value,
                html_content=data.html_content,
                start_date=data.start_date,
                first_payment_due_date=data.first_payment_due_date,
                expiration_date=data.expiration_date,
                education_years=data.education_years,
                is_archived=data.is_archived,
                updated_at=data.updated_at,
                updated_by=data.updated_by.value,
            )
        )
        await self.session.execute(stmt)

    async def delete(
        self, id: IdVO, deleted_by: DeletedByVO, deleted_at: datetime
    ) -> None:
        stmt = (
            update(Contract)
            .where(Contract.id == id.value, Contract.deleted_at.is_(None))
            .values(deleted_by=deleted_by.value, deleted_at=deleted_at)
        )
        await self.session.execute(stmt)

    async def has_contract_in_current_education_year(
        self, student_id: StudentIdVO, current_datetime: datetime
    ) -> bool:

        stmt = select(Contract).where(
            and_(
                Contract.student_id == student_id.value,
                Contract.start_date <= current_datetime,
                Contract.expiration_date > current_datetime,
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.first())

    async def update_contract_download_details(
        self, id: IdVO, download_counter: int, last_downloaded_at: datetime
    ) -> None:
        stmt = (
            update(Contract)
            .where(Contract.id == id.value)
            .values(
                download_counter=download_counter, last_downloaded_at=last_downloaded_at
            )
        )
        await self.session.execute(stmt)

    async def is_contract_number_exists(self, contract_number: str) -> bool:
        stmt = select(Contract.id).where(Contract.number == contract_number)
        result = await self.session.execute(stmt)
        return bool(result.first())
