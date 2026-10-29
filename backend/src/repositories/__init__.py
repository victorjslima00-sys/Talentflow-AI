"""Data access layer with strict multi-tenant isolation.

All database queries must reside in this layer and MUST filter explicitly by
tenant_id on every operation to prevent cross-tenant information disclosure.
"""
