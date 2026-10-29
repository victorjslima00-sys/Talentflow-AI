"""Authentication and registration API endpoints."""

import uuid
from datetime import datetime

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.core.config import settings
from src.models.user import User
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TenantRegisterRequest(BaseModel):
    """Payload for registering a new tenant company with an admin user."""

    company_name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    admin_email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=150)


class LoginRequest(BaseModel):
    """Payload for user authentication."""

    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=128)


class UserResponse(BaseModel):
    """Public representation of a user (hashed_password is strictly excluded)."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RegisterResponse(BaseModel):
    """Response returned upon successful tenant and admin registration."""

    tenant_id: uuid.UUID
    tenant_name: str
    tenant_slug: str
    user: UserResponse


class TokenResponse(BaseModel):
    """Token response returned upon successful authentication."""

    access_token: str
    token_type: str = "bearer"


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Helper attaching secure, HttpOnly authentication cookies to response."""
    is_prod = settings.app_env == "production"
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        max_age=settings.refresh_token_expire_days * 86400,
    )


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register Company and Admin",
)
async def register_company(
    payload: TenantRegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
    """Create a new tenant organization workspace and primary admin account."""
    auth_service = AuthService(db)
    try:
        tenant, user = await auth_service.register_tenant_and_admin(
            company_name=payload.company_name,
            slug=payload.slug,
            admin_email=payload.admin_email,
            password=payload.password,
            full_name=payload.full_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    access_token, refresh_token = auth_service.create_token_pair(user)
    _set_auth_cookies(response, access_token, refresh_token)

    return RegisterResponse(
        tenant_id=tenant.id,
        tenant_name=tenant.name,
        tenant_slug=tenant.slug,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
)
async def login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Authenticate credentials and issue session cookies with JWT."""
    auth_service = AuthService(db)
    try:
        user = await auth_service.authenticate(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    access_token, refresh_token = auth_service.create_token_pair(user)
    _set_auth_cookies(response, access_token, refresh_token)

    return TokenResponse(access_token=access_token)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Session Token",
)
async def refresh_token(
    response: Response,
    refresh_token_cookie: str | None = Cookie(None, alias="refresh_token"),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Refresh session issuing a new access token via HttpOnly refresh cookie."""
    if not refresh_token_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token cookie.",
        )

    auth_service = AuthService(db)
    try:
        new_access_token, _ = await auth_service.refresh_access_token(refresh_token_cookie)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    is_prod = settings.app_env == "production"
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return TokenResponse(access_token=new_access_token)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="User Logout",
)
async def logout(response: Response) -> dict[str, str]:
    """Clear session authentication cookies."""
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully."}


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Current User Profile",
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return profile data of authenticated user within their tenant."""
    return UserResponse.model_validate(current_user)
