from app.domain.exceptions.base import DomainException


class IncorrectAccessTokenException(DomainException):
    """Incorrect access token"""

    pass
