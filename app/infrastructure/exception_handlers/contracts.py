from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.contracts import (
    ContractNotFoundException, StudentAlreadyHasContractException,)


async def contract_not_found_exception_handler(
    request: Request, exc: ContractNotFoundException
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": exc.message})


async def student_already_has_active_contract_exception_handler(
    request: Request, exc: StudentAlreadyHasContractException
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"message": exc.message})
