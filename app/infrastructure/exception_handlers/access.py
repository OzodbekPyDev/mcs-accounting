from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.access import IncorrectAccessTokenException


async def incorrect_access_token_exception_handler(
    request: Request, exc: IncorrectAccessTokenException
):
    return JSONResponse(status_code=403, content={"message": exc.message})
