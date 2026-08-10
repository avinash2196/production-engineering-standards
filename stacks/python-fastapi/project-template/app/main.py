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
        "service.starting service=%s environment=%s",
        settings.service_name,
        settings.environment,
    )
    yield
    logger.info("service.stopping service=%s", settings.service_name)


def create_app() -> FastAPI:
    settings = get_settings()
    return FastAPI(
        title=settings.service_name,
        version="0.1.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
        lifespan=lifespan,
    )


app = create_app()
