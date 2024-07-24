from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.contract_templates import \
    ContractTemplateNotFoundException


async def contract_template_not_found_exception_handler(
    request: Request, exc: ContractTemplateNotFoundException
):
    return JSONResponse(status_code=404, content={"message": exc.message})
