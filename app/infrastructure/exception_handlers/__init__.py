from fastapi import FastAPI
from app.infrastructure.exception_handlers.contracts import (
    contract_not_found_exception_handler,
    student_already_has_active_contract_exception_handler,
)
from app.infrastructure.exception_handlers.faculty_contract_prices import (
    faculty_contract_price_not_found_exception_handler,
)
from app.infrastructure.exception_handlers.contract_templates import (
    contract_template_not_found_exception_handler,
)
from app.infrastructure.exception_handlers.payments import (
    payment_not_found_exception_handler,
    something_went_wrong_while_synchronizing_payments_exception_handler,
)
from app.infrastructure.exception_handlers.pdf_generation import (
    pdf_file_not_generated_exception_handler,
    file_could_not_be_saved_in_docs_exception_handler,
)

from app.domain.exceptions.contracts import (
    ContractNotFoundException,
    StudentAlreadyHasContractException,
)
from app.domain.exceptions.faculty_contract_prices import (
    FacultyContractPriceNotFoundException,
)
from app.domain.exceptions.contract_templates import (
    ContractTemplateNotFoundException,
)
from app.domain.exceptions.payments import (
    PaymentNotFoundException,
    SomethingWentWrongWhileSynchronizingPaymentsException,
)
from app.domain.exceptions.pdf_generation import (
    PdfFileNotGeneratedException,
    FileCouldNotBeSavedInDocsException,
)
from app.domain.exceptions.access import IncorrectAccessTokenException
from app.infrastructure.exception_handlers.access import (
    incorrect_access_token_exception_handler,
)
from app.domain.exceptions.constraints import UniqueConstraintsException
from app.infrastructure.exception_handlers.constraints import (
    unique_constraints_exception_handler,
)


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ContractNotFoundException, handler=contract_not_found_exception_handler
    )
    app.add_exception_handler(
        StudentAlreadyHasContractException,
        handler=student_already_has_active_contract_exception_handler,
    )
    app.add_exception_handler(
        FacultyContractPriceNotFoundException,
        handler=faculty_contract_price_not_found_exception_handler,
    )
    app.add_exception_handler(
        ContractTemplateNotFoundException,
        handler=contract_template_not_found_exception_handler,
    )
    app.add_exception_handler(
        PaymentNotFoundException, handler=payment_not_found_exception_handler
    )
    app.add_exception_handler(
        PdfFileNotGeneratedException,
        handler=pdf_file_not_generated_exception_handler,
    )
    app.add_exception_handler(
        IncorrectAccessTokenException,
        handler=incorrect_access_token_exception_handler,
    )
    app.add_exception_handler(
        UniqueConstraintsException,
        handler=unique_constraints_exception_handler,
    )
    app.add_exception_handler(
        SomethingWentWrongWhileSynchronizingPaymentsException,
        handler=something_went_wrong_while_synchronizing_payments_exception_handler,
    )
    app.add_exception_handler(
        FileCouldNotBeSavedInDocsException,
        handler=file_could_not_be_saved_in_docs_exception_handler,
    )
