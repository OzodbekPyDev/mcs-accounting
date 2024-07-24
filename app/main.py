from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from app.api.v1 import all_routers
from app.infrastructure.config import settings
from app.infrastructure.di.providers.adapters import AdaptersProvider
from app.infrastructure.di.providers.db import DBProvider
from app.infrastructure.di.providers.interactors.contract_templates import \
    ContractTemplatesInteractorProvider
from app.infrastructure.di.providers.interactors.contracts import \
    ContractsInteractorProvider
from app.infrastructure.di.providers.interactors.faculty_contract_prices import \
    FacultyContractPricesInteractorProvider
from app.infrastructure.di.providers.interactors.payments import \
    PaymentsInteractorProvider
from app.infrastructure.di.providers.repositories import RepositoriesProvider
from app.infrastructure.exception_handlers import init_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


app = FastAPI(title="KIUT ACCOUNTING MICROSERVICE", lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def response_any_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # Заменяем raise HTTPException на возвращение JSONResponse
        return JSONResponse(content={"detail": str(e)}, status_code=500)


add_pagination(app)
disable_installed_extensions_check()


for router in all_routers:
    app.include_router(router, prefix=settings.api_prefix)


container = make_async_container(
    DBProvider(),
    RepositoriesProvider(),
    AdaptersProvider(),
    ContractTemplatesInteractorProvider(),
    ContractsInteractorProvider(),
    FacultyContractPricesInteractorProvider(),
    PaymentsInteractorProvider(),
)
setup_dishka(container, app)
init_exception_handlers(app)
