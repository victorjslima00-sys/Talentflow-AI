# Code Standards & Quality Guidelines

1. **Architecture Layers:**
   - `api` (routers, request/response models, HTTP status codes). No business rules here.
   - `services` (business logic, orchestration, validation, calls to external providers).
   - `repositories` (database queries, transactional boundaries, strict `tenant_id` filtering).
2. **Type Safety:**
   - 100% type hints on all functions and methods.
   - Mypy must run in strict mode (`strict = true`) without `# type: ignore` unless specifically justified.
3. **Security & Secrets:**
   - All sensitive configs use `SecretStr`.
   - Never log or return passwords, hashes, tokens, or raw resume texts.
4. **Tenant Isolation:**
   - Every database query in repositories MUST include `tenant_id == current_tenant_id`.
   - Write integration tests proving cross-tenant access returns 404 or 403.
