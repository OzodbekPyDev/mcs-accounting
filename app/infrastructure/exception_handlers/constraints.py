from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.constraints import UniqueConstraintsException


async def unique_constraints_exception_handler(
    request: Request, exc: UniqueConstraintsException
):
    return JSONResponse(status_code=403, content={"message": exc.message})
