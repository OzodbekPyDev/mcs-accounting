from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.faculty_contract_prices import \
    FacultyContractPriceNotFoundException


async def faculty_contract_price_not_found_exception_handler(
    request: Request, exc: FacultyContractPriceNotFoundException
):
    return JSONResponse(status_code=404, content={"message": exc.message})
