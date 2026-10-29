"""Healthcheck endpoint for container orchestration and uptime verification."""

from datetime import UTC, datetime

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from src.core.config import settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check payload schema."""

    status: str = Field(default="healthy", description="Current service health status.")
    version: str = Field(..., description="Application version.")
    environment: str = Field(..., description="Active environment name.")
    timestamp: datetime = Field(..., description="Current UTC timestamp.")


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
    description="Returns current service status, version, environment and UTC timestamp.",
)
async def check_health() -> HealthResponse:
    """Return healthcheck status."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(UTC),
    )
