"""Application configuration with strict validation and secret masking."""

from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Current deployment environment.",
    )
    app_name: str = Field(
        default="TalentFlow AI",
        description="Public name of the application.",
    )
    app_version: str = Field(
        default="0.1.0",
        description="Semantic version of the application.",
    )
    debug: bool = Field(
        default=False,
        description="Debug mode toggle.",
    )

    # Security & Authentication
    secret_key: SecretStr = Field(
        ...,
        description="Cryptographic secret key for signing JWTs and session cookies.",
    )
    access_token_expire_minutes: int = Field(
        default=15,
        ge=5,
        le=60,
        description="Access token lifespan in minutes.",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Refresh token lifespan in days.",
    )

    # Infrastructure
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/talentflow_dev",
        description="PostgreSQL async connection string.",
    )
    redis_url: str = Field(
        default="redis://127.0.0.1:6379/0",
        description="Redis connection string for Celery and caching.",
    )

    # AI Provider
    llm_provider: Literal["mock", "gemini", "openai"] = Field(
        default="mock",
        description="Active LLM provider interface.",
    )
    gemini_api_key: SecretStr | None = Field(
        default=None,
        description="Google Gemini API key.",
    )
    openai_api_key: SecretStr | None = Field(
        default=None,
        description="OpenAI API key.",
    )

    # Server Binding
    host: str = Field(default="127.0.0.1", description="Host interface binding.")
    port: int = Field(default=8000, ge=1, le=65535, description="Port number.")

    @model_validator(mode="after")
    def validate_production_constraints(self) -> "Settings":
        """Enforce strict constraints for production security and integrity."""
        # 1. Enforce minimum secret key length
        secret_val = self.secret_key.get_secret_value()
        if len(secret_val) < 32:
            raise ValueError(
                "SECRET_KEY must be at least 32 characters long for cryptographic security."
            )

        # 2. Prevent accidental execution of mock provider in production
        if self.app_env == "production" and self.llm_provider == "mock":
            raise ValueError(
                "Execution with LLM_PROVIDER=mock is strictly forbidden in production mode."
            )

        # 3. Require provider API key when provider is not mock
        if self.llm_provider == "gemini" and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER is set to 'gemini'.")

        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is set to 'openai'.")

        return self


settings = Settings(
    secret_key=SecretStr("local-dev-secret-key-must-be-at-least-32-chars-long"),
)
