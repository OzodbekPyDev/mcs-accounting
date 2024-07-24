from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate

from app.api.v1.schemes.faculty_contract_prices import (
    DeleteFacultyContractPriceSchema, UpdateFacultyContractPriceSchema,)
from app.application.dto.faculty_contract_prices import (
    CreateFacultyContractPriceRequest, DeleteFacultyContractPriceRequest,
    FacultyContractPriceResponse, GetAllFacultyContractPricesRequest,
    UpdateFacultyContractPriceRequest,)
from app.application.use_cases.faculty_contract_prices.create import \
    CreateFacultyContractPrice
from app.application.use_cases.faculty_contract_prices.delete import \
    DeleteFacultyContractPrice
from app.application.use_cases.faculty_contract_prices.get import (
    GetFacultyContractPriceById, GetListFacultyContractPrices,)
from app.application.use_cases.faculty_contract_prices.update import \
    UpdateFacultyContractPrice


router = APIRouter(
    prefix="/faculty-contract-prices",
    tags=["Faculty Contract Prices"],
    route_class=DishkaRoute,
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_faculty_contract_price(
    request: CreateFacultyContractPriceRequest,
    create_fac_con_price_interactor: FromDishka[CreateFacultyContractPrice],
) -> FacultyContractPriceResponse:
    return await create_fac_con_price_interactor(request)


@router.get("/")
async def get_faculty_contract_prices(
    request: Annotated[GetAllFacultyContractPricesRequest, Depends()],
    get_list_fac_con_prices_interactor: FromDishka[GetListFacultyContractPrices],
) -> Page[FacultyContractPriceResponse]:
    items = await get_list_fac_con_prices_interactor(request)
    return paginate(items)


@router.get("/{id}")
async def get_faculty_contract_price_by_id(
    id: UUID,
    get_fac_con_price_by_id_interactor: FromDishka[GetFacultyContractPriceById],
) -> FacultyContractPriceResponse:
    return await get_fac_con_price_by_id_interactor(id)


@router.put("/{id}")
async def update_faculty_contract_price(
    id: UUID,
    data: UpdateFacultyContractPriceSchema,
    update_fac_con_price_interactor: FromDishka[UpdateFacultyContractPrice],
) -> FacultyContractPriceResponse:

    request = UpdateFacultyContractPriceRequest(
        id=id,
        faculty_id=data.faculty_id,
        amount=data.amount,
        transcriptions=data.transcriptions,
        updated_by=data.updated_by,
    )

    return await update_fac_con_price_interactor(request)


@router.patch("/{id}")
async def delete_faculty_contract_price(
    id: UUID,
    data: DeleteFacultyContractPriceSchema,
    delete_fac_con_price_interactor: FromDishka[DeleteFacultyContractPrice],
) -> dict[str, str]:
    request = DeleteFacultyContractPriceRequest(
        id=id,
        deleted_by=data.deleted_by,
    )
    await delete_fac_con_price_interactor(request)
    return {"message": "Faculty Contract Price deleted successfully"}
