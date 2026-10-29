"""Database configuration, async engine and session management."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models."""


def create_engine_and_session(db_url: str) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Create SQLAlchemy async engine and session factory."""
    connect_args: dict[str, bool] = {}
    if "sqlite" in db_url:
        connect_args["check_same_thread"] = False

    engine = create_async_engine(
        db_url,
        echo=settings.debug,
        future=True,
        connect_args=connect_args,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return engine, session_factory


engine, async_session_factory = create_engine_and_session(settings.database_url)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Provide an asynchronous database session with automatic transaction management."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
