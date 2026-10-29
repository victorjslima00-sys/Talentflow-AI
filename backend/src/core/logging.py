"""Structured JSON logging configuration without sensitive or personal data."""

import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

# Context variable for request correlation tracking
correlation_id_ctx: ContextVar[str | None] = ContextVar("correlation_id", default=None)

# Sensitive patterns that must never appear in logs
SENSITIVE_KEYS = {
    "password",
    "secret",
    "token",
    "hashed_password",
    "authorization",
    "cookie",
    "cpf",
    "email",
    "phone",
    "resume",
    "extracted_text",
}


class JSONFormatter(logging.Formatter):
    """Custom formatter producing single-line JSON log events."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Append correlation ID if active in context
        cid = correlation_id_ctx.get()
        if cid:
            log_payload["correlation_id"] = cid

        # Include exception information if available
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload)


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger with the structured JSON formatter."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing default handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)
