from app.domain.exceptions.base import DomainException


class UniqueConstraintsException(DomainException):
    """Unique constraints violation exception"""

    pass
