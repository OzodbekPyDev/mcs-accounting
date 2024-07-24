from app.domain.exceptions.base import DomainException


class ContractTemplateNotFoundException(DomainException):
    """Contract template not found"""

    pass
