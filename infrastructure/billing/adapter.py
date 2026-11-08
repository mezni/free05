"""Billing adapter for bss-core Support Application."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from infrastructure.config import get_settings


def mask_sensitive_data(
    card_number: str,
    mask_from: int = 12,
) -> str:
    """Mask sensitive card data for PCI-DSS compliance.

    AD-4: Payment data must be masked at boundary; never store full PAN.
    FR-19: System MUST store payment method masks only (e.g. "Visa ending in 4242").
    FR-24: System MUST return only masked payment data (PCI-DSS compliant).
    """
    if not card_number:
        return "No card data"

    # Mask all but last 4 digits
    if len(card_number) <= mask_from:
        return "XXX" * mask_from

    visible = card_number[-4:]
    masked = "X" * (len(card_number) - mask_from)
    return f"{masked}{visible}"


def format_currency_amount(
    amount: Decimal,
) -> str:
    """Format amount as string for serialization.

    Decision from research.md: Use Decimal in domain, persist as NUMERIC,
    serialize as a string to avoid floating point drift.
    """
    return f"{amount:.2f}"


def get_settings() -> dict:
    """Get billing configuration settings."""
    return get_settings()