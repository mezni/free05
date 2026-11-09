"""FastAPI application entry point for bss-core Support Application."""

from fastapi import FastAPI

from api.routes.customers import router as customers_router
from api.routes.orders import router as orders_router
from api.routes.billing import router as billing_router
from api.routes.returns import router as returns_router
from api.routes.shipments import router as shipments_router
from api.routes.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="bss-core Support Application API",
        version="0.1.0",
        description="Hexagonal (ports-and-adapters) Python support application",
    )

    app.include_router(customers_router)
    app.include_router(orders_router)
    app.include_router(billing_router)
    app.include_router(returns_router)
    app.include_router(shipments_router)
    app.include_router(users_router)

    return app


app = create_app()