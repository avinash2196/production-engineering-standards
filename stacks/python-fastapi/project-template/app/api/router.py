from pydantic import BaseModel

from fastapi import APIRouter

from app.config.settings import get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


@router.get("/health", response_model=HealthResponse, tags=["ops"])
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="UP",
        service=settings.service_name,
        environment=settings.environment,
    )


@router.get("/health/live", status_code=200, tags=["ops"])
async def liveness() -> dict[str, str]:
    """Kubernetes liveness probe — returns UP if the process is running."""
    return {"status": "UP"}


@router.get("/health/ready", status_code=200, tags=["ops"])
async def readiness() -> dict[str, str]:
    """Kubernetes readiness probe — add DB/cache checks here."""
    # TODO: inject and check DatabaseHealthIndicator, CacheHealthIndicator
    return {"status": "UP"}
