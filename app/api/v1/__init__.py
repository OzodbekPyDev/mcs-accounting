from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.contract_templates import (
    router as contract_templates_router,
)
from app.api.v1.routers.faculty_contract_prices import (
    router as faculty_contract_prices_router,
)
from app.api.v1.routers.contracts import router as contracts_router
from app.api.v1.routers.payments import router as payments_router

all_routers = [
    health_router,
    contract_templates_router,
    faculty_contract_prices_router,
    contracts_router,
    payments_router,
]
