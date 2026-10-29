"""Tenant information API endpoints."""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from src.api.deps import get_current_tenant
from src.models.tenant import Tenant

router = APIRouter(prefix="/tenants", tags=["Tenants"])


class TenantResponse(BaseModel):
    """Public representation of a tenant company workspace."""

    id: uuid.UUID
    name: str
    slug: str
    plan: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get(
    "/me",
    response_model=TenantResponse,
    status_code=status.HTTP_200_OK,
    summary="Current Tenant Workspace",
)
async def get_current_tenant_workspace(
    tenant: Tenant = Depends(get_current_tenant),
) -> TenantResponse:
    """Return the organization workspace tied to the current authenticated user."""
    return TenantResponse.model_validate(tenant)
