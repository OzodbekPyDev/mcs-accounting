from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Header, status
from fastapi_pagination import Page, paginate

from app.application.dto.payments import (CreatePaymentRequest,
                                          GetListPaymentsRequest,
                                          PaymentResponse,
                                          SynchronizationPaymentsResponse)
from app.application.use_cases.payments.create import CreatePayment
from app.application.use_cases.payments.delete import DeleteAllPayments
from app.application.use_cases.payments.get import (GetListPayments,
                                                    GetPaymentById,)
from app.application.use_cases.payments.synchronize_data import \
    SynchronizePaymentsData
from app.domain.exceptions.access import IncorrectAccessTokenException
from app.infrastructure.config import settings


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    route_class=DishkaRoute,
)


@router.post("/1c/", status_code=status.HTTP_201_CREATED)
async def create_payment(
    request: CreatePaymentRequest,
    create_payment_interactor: FromDishka[CreatePayment],
    Authentication: Annotated[str, Header()],
) -> dict[str, str]:
    if Authentication != settings.ACCESS_PAYMENTS_TOKEN:
        raise IncorrectAccessTokenException(
            "Incorrect access token or access token not provided"
        )

    await create_payment_interactor(request)
    return {"message": "Payment created successfully"}


@router.get("/synchronize")
async def synchronize_payments(
    synchronize_payments_data_interactor: FromDishka[SynchronizePaymentsData],
) -> SynchronizationPaymentsResponse:
    return await synchronize_payments_data_interactor(None)


@router.get("/")
async def get_payments(
    request: Annotated[GetListPaymentsRequest, Depends()],
    get_list_payments_interactor: FromDishka[GetListPayments],
) -> Page[PaymentResponse]:
    items = await get_list_payments_interactor(request)
    return paginate(items)


@router.get("/{id}")
async def get_payment_by_id(
    id: UUID,
    get_payment_by_id_interactor: FromDishka[GetPaymentById],
) -> PaymentResponse:
    return await get_payment_by_id_interactor(id)


@router.delete("/delete_all")
async def delete_all_payments(
    delete_all_payments_interactor: FromDishka[DeleteAllPayments],
) -> dict[str, str]:
    await delete_all_payments_interactor(request=None)
    return {"message": "All payments deleted successfully"}
