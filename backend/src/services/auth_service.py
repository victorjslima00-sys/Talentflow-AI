"""Authentication, session management and credential validation service."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from src.models.tenant import Tenant
from src.models.user import User
from src.repositories.tenant_repository import TenantRepository
from src.repositories.user_repository import UserRepository
from src.services.tenant_service import TenantService


class AuthService:
    """Service handling registration, credential checks, and token lifecycle."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.tenant_repo = TenantRepository(session)
        self.tenant_service = TenantService(session)

    async def register_tenant_and_admin(
        self,
        company_name: str,
        slug: str,
        admin_email: str,
        password: str,
        full_name: str,
    ) -> tuple[Tenant, User]:
        """Register a new tenant company and its primary administrator account."""
        if len(password) < 8:
            raise ValueError("Password must have at least 8 characters.")

        # 1. Create tenant (validates slug uniqueness)
        tenant = await self.tenant_service.create_tenant(name=company_name, slug=slug)

        # 2. Check if user already exists
        existing_user = await self.user_repo.get_by_email_global(admin_email)
        if existing_user:
            raise ValueError(f"User with email '{admin_email}' is already registered.")

        # 3. Hash password with Argon2id and create admin user
        hashed = get_password_hash(password)
        user = await self.user_repo.create(
            tenant_id=tenant.id,
            email=admin_email,
            hashed_password=hashed,
            full_name=full_name,
            role="admin",
        )
        return tenant, user

    async def authenticate(self, email: str, password: str) -> User:
        """Authenticate user credentials and return the active User entity."""
        user = await self.user_repo.get_by_email_global(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        if not user.is_active:
            raise ValueError("User account is deactivated.")

        return user

    def create_token_pair(self, user: User) -> tuple[str, str]:
        """Generate access and refresh tokens embedding user and tenant claims."""
        token_data = {
            "sub": str(user.id),
            "tenant_id": str(user.tenant_id),
            "role": user.role,
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        return access_token, refresh_token

    async def refresh_access_token(self, refresh_token: str) -> tuple[str, User]:
        """Validate refresh token and issue a fresh access token."""
        try:
            payload = decode_token(refresh_token)
        except Exception as exc:
            raise ValueError("Invalid or expired refresh token.") from exc

        if payload.get("type") != "refresh":
            raise ValueError("Provided token is not a refresh token.")

        user_id = uuid.UUID(payload["sub"])
        tenant_id = uuid.UUID(payload["tenant_id"])

        user = await self.user_repo.get_by_id(tenant_id=tenant_id, entity_id=user_id)
        if not user or not user.is_active:
            raise ValueError("User account not found or deactivated.")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "tenant_id": str(user.tenant_id),
                "role": user.role,
            }
        )
        return access_token, user
