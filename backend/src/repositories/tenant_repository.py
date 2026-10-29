"""Tenant data access repository."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.tenant import Tenant


class TenantRepository:
    """Repository handling persistence and queries for Tenant entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, tenant_id: uuid.UUID) -> Tenant | None:
        """Fetch a tenant by primary key."""
        statement = select(Tenant).where(Tenant.id == tenant_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Tenant | None:
        """Fetch a tenant by its unique slug."""
        statement = select(Tenant).where(Tenant.slug == slug)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, name: str, slug: str, plan: str = "free") -> Tenant:
        """Persist a new Tenant entity."""
        tenant = Tenant(name=name, slug=slug, plan=plan)
        self.session.add(tenant)
        await self.session.flush()
        return tenant
