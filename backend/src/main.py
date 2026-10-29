"""Main FastAPI application entry point."""

import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.v1.health import router as health_router
from src.core.config import settings
from src.core.logging import correlation_id_ctx, setup_logging


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware attaching a unique correlation ID to every incoming request."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        token = correlation_id_ctx.set(cid)
        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = cid
            return response
        finally:
            correlation_id_ctx.reset(token)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager for startup and shutdown routines."""
    setup_logging(level="DEBUG" if settings.debug else "INFO")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-tenant ATS SaaS with AI-powered candidate evaluation.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Cross-Origin Resource Sharing (CORS) - restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"]
    if settings.app_env != "production"
    else [],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(CorrelationIDMiddleware)

# Register health check routes
app.include_router(health_router)
app.include_router(health_router, prefix="/api/v1")
