from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate

from app.api.v1.schemes.contracts import UpdateContractSchema
from app.application.dto.contracts import (ContractResponse,
                                           CreateContractRequest,
                                           GetListContractsRequest,
                                           StudentContractInfoResponse,
                                           UpdateContractRequest,)
from app.application.use_cases.contracts.create import CreateContract
from app.application.use_cases.contracts.get import (GetContractById,
                                                     GetListContracts,)
from app.application.use_cases.contracts.update import (
    UpdateContract, UpdateContractDownloadDetails,)


router = APIRouter(prefix="/contracts", tags=["Contracts"], route_class=DishkaRoute)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_contract(
    request: CreateContractRequest,
    create_contract_interactor: FromDishka[CreateContract],
) -> StudentContractInfoResponse:
    return await create_contract_interactor(request)


@router.get("/")
async def get_contracts(
    request: Annotated[GetListContractsRequest, Depends()],
    get_list_contracts_interactor: FromDishka[GetListContracts],
) -> Page[ContractResponse]:
    items = await get_list_contracts_interactor(request)
    return paginate(items)


@router.get("/{id}")
async def get_contract_by_id(
    id: UUID, get_contract_by_id_interactor: FromDishka[GetContractById]
) -> ContractResponse:
    return await get_contract_by_id_interactor(id)


@router.put("/{id}")
async def update_contract(
    id: UUID,
    data: UpdateContractSchema,
    update_contract_interactor: FromDishka[UpdateContract],
) -> ContractResponse:

    request = UpdateContractRequest(
        id=id,
        template_id=data.template_id,
        html_content=data.html_content,
        start_date=data.start_date,
        first_payment_due_date=data.first_payment_due_date,
        expiration_date=data.expiration_date,
        is_archived=data.is_archived,
        updated_by=data.updated_by,
        education_years=data.education_years
    )

    return await update_contract_interactor(request)


@router.put("/{id}/download")
async def update_contract_download_details(
    id: UUID,
    update_contract_download_details_interactor: FromDishka[
        UpdateContractDownloadDetails
    ],
) -> dict[str, str]:
    await update_contract_download_details_interactor(id)
    return {"message": "Contract download details updated successfully."}
