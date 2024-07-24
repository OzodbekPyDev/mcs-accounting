from app.domain.exceptions.base import DomainException


class PdfFileNotGeneratedException(DomainException):
    """Pdf file not generated"""

    pass


class FileCouldNotBeSavedInDocsException(DomainException):
    """File could not be saved"""

    pass
