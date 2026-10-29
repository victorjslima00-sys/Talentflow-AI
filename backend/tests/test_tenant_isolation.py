"""Critical cross-tenant isolation and data segregation tests (BOLA prevention)."""

import uuid

import pytest
from httpx import AsyncClient

from src.repositories.user_repository import UserRepository
from tests.conftest import db_session_factory


@pytest.mark.asyncio
async def test_tenant_workspace_isolation(async_client: AsyncClient) -> None:
    """Verify that User A cannot see or access Tenant B's organization data."""
    # 1. Register Company A
    payload_a = {
        "company_name": "Company Alpha",
        "slug": "company-alpha",
        "admin_email": "admin@alpha.com",
        "password": "AlphaPassword123!",
        "full_name": "Alpha Admin",
    }
    resp_a = await async_client.post("/api/v1/auth/register", json=payload_a)
    assert resp_a.status_code == 201
    tenant_a_id = resp_a.json()["tenant_id"]

    # Login User A
    login_a = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@alpha.com", "password": "AlphaPassword123!"},
    )
    token_a = login_a.json()["access_token"]

    # 2. Register Company B
    payload_b = {
        "company_name": "Company Beta",
        "slug": "company-beta",
        "admin_email": "admin@beta.com",
        "password": "BetaPassword123!",
        "full_name": "Beta Admin",
    }
    resp_b = await async_client.post("/api/v1/auth/register", json=payload_b)
    assert resp_b.status_code == 201
    tenant_b_id = resp_b.json()["tenant_id"]

    # Login User B
    login_b = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@beta.com", "password": "BetaPassword123!"},
    )
    token_b = login_b.json()["access_token"]

    # 3. User A queries /tenants/me
    me_tenant_a = await async_client.get(
        "/api/v1/tenants/me",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert me_tenant_a.status_code == 200
    assert me_tenant_a.json()["id"] == tenant_a_id
    assert me_tenant_a.json()["slug"] == "company-alpha"

    # 4. User B queries /tenants/me
    me_tenant_b = await async_client.get(
        "/api/v1/tenants/me",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert me_tenant_b.status_code == 200
    assert me_tenant_b.json()["id"] == tenant_b_id
    assert me_tenant_b.json()["slug"] == "company-beta"

    # Verify that IDs are completely distinct
    assert me_tenant_a.json()["id"] != me_tenant_b.json()["id"]


@pytest.mark.asyncio
async def test_repository_strictly_blocks_cross_tenant_access(
    async_client: AsyncClient,
) -> None:
    """Verify at the repository level that querying with Tenant B's ID returns None for Tenant A's user."""
    # 1. Register Company A
    reg_a = await async_client.post(
        "/api/v1/auth/register",
        json={
            "company_name": "Corp X",
            "slug": "corp-x",
            "admin_email": "user@corp-x.com",
            "password": "PasswordCorpX123!",
            "full_name": "User X",
        },
    )
    user_a_id = uuid.UUID(reg_a.json()["user"]["id"])
    tenant_a_id = uuid.UUID(reg_a.json()["tenant_id"])

    # 2. Register Company B
    reg_b = await async_client.post(
        "/api/v1/auth/register",
        json={
            "company_name": "Corp Y",
            "slug": "corp-y",
            "admin_email": "user@corp-y.com",
            "password": "PasswordCorpY123!",
            "full_name": "User Y",
        },
    )
    tenant_b_id = uuid.UUID(reg_b.json()["tenant_id"])

    # 3. Direct repository query cross-check
    async with db_session_factory() as session:
        repo = UserRepository(session)

        # Querying User A under Tenant A -> FOUND
        found_user = await repo.get_by_id(tenant_id=tenant_a_id, entity_id=user_a_id)
        assert found_user is not None
        assert found_user.email == "user@corp-x.com"

        # Querying User A under Tenant B -> NOT FOUND (Strict Isolation Enforced)
        cross_tenant_user = await repo.get_by_id(tenant_id=tenant_b_id, entity_id=user_a_id)
        assert cross_tenant_user is None
