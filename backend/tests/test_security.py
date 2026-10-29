"""Tests for Argon2id hashing and PyJWT token utilities."""

from datetime import UTC, datetime, timedelta

import jwt
import pytest

from src.core.security import (
    ALGORITHM,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)


def test_argon2id_hashing_and_verification() -> None:
    """Verify that passwords are hash-verified correctly and mismatches fail."""
    password = "SuperSecurePassword123!"
    hashed = get_password_hash(password)

    # Hash must start with Argon2id signature
    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_access_token_creation_and_payload() -> None:
    """Verify that generated JWT tokens contain valid claims and UTC timestamps."""
    data = {"sub": "user-uuid-1", "tenant_id": "tenant-uuid-1", "role": "admin"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))

    payload = decode_token(token)
    assert payload["sub"] == "user-uuid-1"
    assert payload["tenant_id"] == "tenant-uuid-1"
    assert payload["role"] == "admin"
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "iat" in payload


def test_jwt_refresh_token_creation_and_payload() -> None:
    """Verify that refresh tokens contain refresh type and claims."""
    data = {"sub": "user-uuid-1", "tenant_id": "tenant-uuid-1"}
    token = create_refresh_token(data, expires_delta=timedelta(days=7))

    payload = decode_token(token)
    assert payload["sub"] == "user-uuid-1"
    assert payload["tenant_id"] == "tenant-uuid-1"
    assert payload["type"] == "refresh"


def test_jwt_expired_token_raises_exception() -> None:
    """Verify that expired tokens are strictly rejected."""
    expired_time = datetime.now(UTC) - timedelta(minutes=5)
    expired_token = jwt.encode(
        {"sub": "user-1", "type": "access", "exp": expired_time},
        "local-dev-secret-key-must-be-at-least-32-chars-long",
        algorithm=ALGORITHM,
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(expired_token)
