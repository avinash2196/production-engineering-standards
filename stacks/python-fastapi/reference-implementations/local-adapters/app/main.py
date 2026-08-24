"""Runnable shell for the local-adapter reference implementation."""

from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

from fastapi import FastAPI

from app.config.settings import get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logger.info(
        "reference.starting service=%s environment=%s messaging=%s cache=%s storage=%s secrets=%s",
        settings.service_name,
        settings.environment,
        settings.messaging_adapter.value,
        settings.cache_adapter.value,
        settings.storage_adapter.value,
        settings.secret_adapter.value,
    )
    yield
    logger.info("reference.stopping service=%s", settings.service_name)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=f"{settings.service_name} local-adapter reference",
        version="0.1.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
        lifespan=lifespan,
    )
    return app


app = create_app()
