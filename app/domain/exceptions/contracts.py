from app.domain.exceptions.base import DomainException


class StudentAlreadyHasContractException(DomainException):
    """Student already has an active contract"""

    pass


class ContractNotFoundException(DomainException):
    """Contract not found"""

    pass
