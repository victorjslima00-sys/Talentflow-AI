"""Tests for the service health check endpoint."""

import pytest
from httpx import AsyncClient

from src.core.config import settings


@pytest.mark.asyncio
async def test_health_check_returns_ok_and_metadata(async_client: AsyncClient) -> None:
    """Verify that /health responds with 200 OK and valid health payload."""
    response = await async_client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["version"] == settings.app_version
    assert data["environment"] == settings.app_env
    assert "timestamp" in data
    assert "x-correlation-id" in response.headers


@pytest.mark.asyncio
async def test_health_check_v1_prefix_parity(async_client: AsyncClient) -> None:
    """Verify that /api/v1/health responds identically to /health."""
    response = await async_client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_check_propagates_custom_correlation_id(
    async_client: AsyncClient,
) -> None:
    """Verify that an incoming X-Correlation-ID header is preserved and echoed."""
    custom_cid = "test-correlation-uuid-12345"
    response = await async_client.get("/health", headers={"X-Correlation-ID": custom_cid})

    assert response.status_code == 200
    assert response.headers.get("x-correlation-id") == custom_cid
