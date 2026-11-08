"""Environment configuration with defaults for bss-core Support Application."""

import os
from decimal import Decimal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def get_settings():
    """Return configuration as a namespace object."""
    return {
        "database_url": os.getenv("BSS_DATABASE_URL", str(BASE_DIR / "bss.db")),
        "jwt_secret": os.getenv("BSS_JWT_SECRET", "dev-only-secret-must-change"),
        "jwt_ttl_seconds": int(os.getenv("BSS_JWT_TTL_SECONDS", "86400")),
        "return_window_days": int(os.getenv("BSS_RETURN_WINDOW_DAYS", "30")),
        "max_qty_per_line": os.getenv("BSS_MAX_QTY_PER_LINE"),
        "environment": os.getenv("BSS_ENV", "development"),
    }


# Export for direct import
settings = get_settings()