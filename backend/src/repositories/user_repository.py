"""User data access repository with strict tenant boundaries."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.base import BaseTenantRepository


class UserRepository(BaseTenantRepository[User]):
    """Repository handling persistence and queries for User entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, tenant_id: uuid.UUID, email: str) -> User | None:
        """Fetch user by email within the boundaries of a specific tenant."""
        statement = select(User).where(
            User.tenant_id == tenant_id,
            func.lower(User.email) == email.lower().strip(),
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email_global(self, email: str) -> User | None:
        """Find user by email across all tenants for initial login resolution."""
        statement = select(User).where(func.lower(User.email) == email.lower().strip())
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(
        self,
        tenant_id: uuid.UUID,
        email: str,
        hashed_password: str,
        full_name: str,
        role: str = "recruiter",
    ) -> User:
        """Persist a new User entity tied strictly to tenant_id."""
        user = User(
            tenant_id=tenant_id,
            email=email.lower().strip(),
            hashed_password=hashed_password,
            full_name=full_name.strip(),
            role=role,
        )
        self.session.add(user)
        await self.session.flush()
        return user
