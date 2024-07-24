from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.payments import (
    PaymentNotFoundException,
    SomethingWentWrongWhileSynchronizingPaymentsException,)


async def payment_not_found_exception_handler(
    request: Request, exc: PaymentNotFoundException
):
    return JSONResponse(status_code=404, content={"message": exc.message})


async def something_went_wrong_while_synchronizing_payments_exception_handler(
    request: Request,
    exc: SomethingWentWrongWhileSynchronizingPaymentsException,
):
    return JSONResponse(status_code=500, content={"message": exc.message})
