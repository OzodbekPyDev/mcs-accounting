from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.pdf_generation import (
    FileCouldNotBeSavedInDocsException, PdfFileNotGeneratedException,)


async def pdf_file_not_generated_exception_handler(
    request: Request, exc: PdfFileNotGeneratedException
):
    return JSONResponse(status_code=400, content={"message": exc.message})


async def file_could_not_be_saved_in_docs_exception_handler(
    request: Request, exc: FileCouldNotBeSavedInDocsException
):
    return JSONResponse(status_code=400, content={"message": exc.message})
