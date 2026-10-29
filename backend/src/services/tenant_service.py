"""Tenant management business logic."""

import re
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.tenant import Tenant
from src.repositories.tenant_repository import TenantRepository


class TenantService:
    """Service handling organization workspaces and tenant lifecycle."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = TenantRepository(session)

    async def get_by_id(self, tenant_id: uuid.UUID) -> Tenant:
        """Fetch tenant by ID or raise an error if not found."""
        tenant = await self.repository.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant organization not found.")
        return tenant

    async def create_tenant(self, name: str, slug: str, plan: str = "free") -> Tenant:
        """Create a new tenant validating slug uniqueness and format."""
        clean_slug = re.sub(r"[^a-z0-9\-]", "", slug.lower().strip())
        if not clean_slug:
            raise ValueError("Invalid slug format. Must contain only alphanumeric characters.")

        existing = await self.repository.get_by_slug(clean_slug)
        if existing:
            raise ValueError(f"Organization slug '{clean_slug}' is already registered.")

        return await self.repository.create(name=name.strip(), slug=clean_slug, plan=plan)
