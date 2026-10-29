"""Base repository enforcing strict multi-tenant isolation on all queries."""

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import TenantScopedModel


class BaseTenantRepository[ModelType: TenantScopedModel]:
    """Generic repository enforcing tenant_id filtering on every query."""

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, tenant_id: uuid.UUID, entity_id: uuid.UUID) -> ModelType | None:
        """Fetch a single entity verifying both entity_id and tenant_id."""
        statement = select(self.model).where(
            self.model.id == entity_id,
            self.model.tenant_id == tenant_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_by_tenant(
        self, tenant_id: uuid.UUID, limit: int = 50, offset: int = 0
    ) -> Sequence[ModelType]:
        """List entities belonging exclusively to the specified tenant."""
        statement = (
            select(self.model).where(self.model.tenant_id == tenant_id).limit(limit).offset(offset)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
