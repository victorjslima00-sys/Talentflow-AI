"""Integration tests for authentication, tenant onboarding and session flows."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_tenant_and_admin_sets_cookies(async_client: AsyncClient) -> None:
    """Verify that registering a company creates tenant, user, and sets HttpOnly cookies."""
    payload = {
        "company_name": "Acme Corp",
        "slug": "acme-corp",
        "admin_email": "admin@acme.com",
        "password": "SuperSecretPassword123!",
        "full_name": "Alice Administrator",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["tenant_name"] == "Acme Corp"
    assert data["tenant_slug"] == "acme-corp"
    assert data["user"]["email"] == "admin@acme.com"
    assert data["user"]["role"] == "admin"

    # CRITICAL: hashed_password must NEVER be returned in any response
    assert "hashed_password" not in data["user"]
    assert "password" not in data["user"]

    # Verify cookies
    cookies = response.cookies
    assert "access_token" in cookies
    assert "refresh_token" in cookies


@pytest.mark.asyncio
async def test_duplicate_registration_slug_rejected(async_client: AsyncClient) -> None:
    """Verify that registering with an already existing slug returns 400 Bad Request."""
    payload = {
        "company_name": "First Corp",
        "slug": "unique-slug",
        "admin_email": "first@corp.com",
        "password": "Password123!",
        "full_name": "First User",
    }
    r1 = await async_client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201

    duplicate_payload = {
        "company_name": "Second Corp",
        "slug": "unique-slug",
        "admin_email": "second@corp.com",
        "password": "Password123!",
        "full_name": "Second User",
    }
    r2 = await async_client.post("/api/v1/auth/register", json=duplicate_payload)
    assert r2.status_code == 400
    assert "already registered" in r2.json()["detail"]


@pytest.mark.asyncio
async def test_login_flow_and_me_endpoint(async_client: AsyncClient) -> None:
    """Verify user login with valid credentials and fetching /me profile."""
    # 1. Register tenant
    reg_payload = {
        "company_name": "Beta Labs",
        "slug": "beta-labs",
        "admin_email": "recruiter@beta.com",
        "password": "ValidPassword999!",
        "full_name": "Bob Recruiter",
    }
    await async_client.post("/api/v1/auth/register", json=reg_payload)

    # 2. Login
    login_payload = {
        "email": "recruiter@beta.com",
        "password": "ValidPassword999!",
    }
    login_resp = await async_client.post("/api/v1/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    assert token is not None

    # 3. Call /me with Bearer token
    me_resp = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "recruiter@beta.com"


@pytest.mark.asyncio
async def test_login_with_invalid_credentials_rejected(async_client: AsyncClient) -> None:
    """Verify that wrong password returns 401 Unauthorized."""
    payload = {
        "email": "nonexistent@user.com",
        "password": "RandomPassword123!",
    }
    response = await async_client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_unauthenticated_request_rejected(async_client: AsyncClient) -> None:
    """Verify that requests without credentials to protected routes return 401."""
    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401
