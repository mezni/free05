"""Database initialization: create all SQLAlchemy tables in SQLite."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.db.models import Base
from infrastructure.db import _ensure_sqlite_url
from infrastructure.config import get_settings


def init_db(database_url: str | None = None) -> None:
    """Create all SQLite tables based on SQLAlchemy model definitions.

    Args:
        database_url: SQLite file path. Defaults to BSS_DATABASE_URL env or bss.db.
    """
    settings = get_settings()
    url = _ensure_sqlite_url(database_url or settings["database_url"])
    engine = create_engine(url, future=True)
    Base.metadata.create_all(engine)