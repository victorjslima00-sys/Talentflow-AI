"""FastAPI request dependencies for database sessions, authentication, and tenant context."""

import uuid
from collections.abc import AsyncIterator

from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.core.security import decode_token
from src.models.tenant import Tenant
from src.models.user import User
from src.repositories.tenant_repository import TenantRepository
from src.repositories.user_repository import UserRepository


async def get_db() -> AsyncIterator[AsyncSession]:
    """Dependency yielding a transactional asynchronous database session."""
    async for session in get_db_session():
        yield session


async def get_token_from_request(
    request: Request,
    access_token_cookie: str | None = Cookie(None, alias="access_token"),
) -> str:
    """Extract JWT token from Authorization Bearer header or HttpOnly cookie."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:].strip()

    if access_token_cookie:
        return access_token_cookie

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Missing token header or cookie.",
    )


async def get_current_user(
    token: str = Depends(get_token_from_request),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Validate JWT token and return authenticated User strictly within their tenant."""
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        ) from exc

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    user_id_raw = payload.get("sub")
    tenant_id_raw = payload.get("tenant_id")
    if not user_id_raw or not tenant_id_raw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing required claims.",
        )

    user_id = uuid.UUID(user_id_raw)
    tenant_id = uuid.UUID(tenant_id_raw)

    repo = UserRepository(db)
    user = await repo.get_by_id(tenant_id=tenant_id, entity_id=user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or account is inactive.",
        )

    return user


async def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    """Return the active Tenant organization tied to the authenticated user."""
    repo = TenantRepository(db)
    tenant = await repo.get_by_id(current_user.tenant_id)
    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization workspace is inactive or suspended.",
        )
    return tenant
