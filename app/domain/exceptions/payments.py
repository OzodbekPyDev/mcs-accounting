from app.domain.exceptions.base import DomainException


class PaymentNotFoundException(DomainException):
    """Payment not found"""

    pass


class SomethingWentWrongWhileSynchronizingPaymentsException(DomainException):
    """Something went wrong while synchronizing payments"""

    pass
