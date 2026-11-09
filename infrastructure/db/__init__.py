"""SQLite database engine and session configuration for bss-core."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import URL

from infrastructure.config import get_settings


def _make_engine() -> "create_engine":
    """Create SQLAlchemy engine from settings."""
    settings = get_settings()
    url = _ensure_sqlite_url(settings["database_url"])
    return create_engine(url, echo=False, future=True)


def _ensure_sqlite_url(url: str) -> str:
    """Ensure the URL has the sqlite:/// prefix for file paths."""
    if url.startswith("sqlite:") or url.startswith("sqlite://"):
        return url
    # Absolute file path -> sqlite:/// path
    if not url.startswith("sqlite://"):
        return "sqlite:///" + url
    return url


engine = _make_engine()
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_session() -> Session:
    """Dependency-injected SQLAlchemy session."""
    return SessionLocal()