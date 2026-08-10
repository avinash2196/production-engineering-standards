from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI

from app.api.router import router
from app.config.settings import get_settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logger.info(
        "service.starting",
        service=settings.service_name,
        environment=settings.environment,
        messaging_adapter=settings.messaging_adapter.value,
        cache_adapter=settings.cache_adapter.value,
        storage_adapter=settings.storage_adapter.value,
        secret_adapter=settings.secret_adapter.value,
    )
    yield
    logger.info("service.stopping", service=settings.service_name)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.service_name,
        version="0.1.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.include_router(router)

    # Add metrics and distributed tracing only when the approved service design
    # requires them and the selected production runtime supports the mechanism.
    return app


app = create_app()
