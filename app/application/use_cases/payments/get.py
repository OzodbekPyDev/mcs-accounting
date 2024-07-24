from uuid import UUID

from app.application.dto.payments import (GetListPaymentsRequest,
                                          PaymentResponse,)
from app.application.protocols.interactor import Interactor
from app.domain.exceptions.payments import PaymentNotFoundException
from app.domain.protocols.repositories.payments import IPaymentsRepository
from app.domain.value_objects.id import IdVO

from app.domain.entities.filter_params.payments import PaymentsFilterParams


class GetListPayments(Interactor[GetListPaymentsRequest, list[PaymentResponse]]):

    def __init__(
        self,
        payments_repository: IPaymentsRepository,
    ) -> None:
        self.payments_repository = payments_repository

    async def __call__(self, request: GetListPaymentsRequest) -> list[PaymentResponse]:
        payments = await self.payments_repository.get_all(
            filter_params=PaymentsFilterParams(
                passport_number=request.passport_number,
                contract_number=request.contract_number,
                pinfl=request.pinfl
            )
        )
        return [PaymentResponse.from_entity(payment) for payment in payments]


class GetPaymentById(Interactor[UUID, PaymentResponse]):

    def __init__(
        self,
        payments_repository: IPaymentsRepository,
    ) -> None:
        self.payments_repository = payments_repository

    async def __call__(self, request: UUID) -> PaymentResponse:
        payment = await self.payments_repository.get_by_id(id=IdVO(value=request))
        if not payment:
            raise PaymentNotFoundException("Payment not found")
        return PaymentResponse.from_entity(payment)
