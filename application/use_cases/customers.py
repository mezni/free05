"""Customer use cases for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from domain.entities import Customer, Tier
from domain.policies import can_modify_tier


def create_customer(
    *,
    name: str,
    email: str,
    tier: Tier = Tier.Standard,
    preferences: dict | None = None,
) -> Customer:
    """Create a new customer.

    FR-01: System MUST create, read, update, and delete customers.
    FR-02: System MUST assign a tier of Standard, Gold, or Enterprise.
    FR-21: System MUST retrieve non-sensitive profile details (name, email, preferences).
    """
    if not name or not name.strip():
        raise ValueError("Customer name must not be empty")
    if not email or "@" not in email:
        raise ValueError("Customer email must be valid")

    customer = Customer(
        name=name.strip(),
        email=email.strip(),
        tier=tier,
        preferences=preferences or {},
        created_at=datetime.now(datetime.utcnow().tzinfo if hasattr(datetime, "utcnow") else None),
        updated_at=datetime.now(datetime.utcnow().tzinfo if hasattr(datetime, "utcnow") else None),
    )
    return customer


def update_customer_tier(
    customer: Customer,
    new_tier: Tier,
) -> Customer:
    """Update customer tier.

    FR-02: System MUST assign a tier of Standard, Gold, or Enterprise.
    NFR-07: Email MUST be unique for customers and users.
    """
    if not can_modify_tier(customer, new_tier):
        raise ValueError(f"Cannot modify customer tier from {customer.tier} to {new_tier}")
    customer.tier = new_tier
    customer.updated_at = datetime.now()
    return customer


def get_customer_by_email(
    email: str,
) -> Optional[Customer]:
    """Get customer by email (for repository pattern)."""
    # This is a placeholder - actual lookup would be via repository
    return None


def list_customers(
    *,
    tier: Tier | None = None,
    name_filter: str | None = None,
) -> list[Customer]:
    """List customers with optional tier filter and name search.

    FR-03: System MUST search customers by name or email.
    FR-05: System MUST filter customers by tier.
    """
    # Placeholder - actual implementation would query repository
    return []


def get_customer_profile(
    customer: Customer,
) -> dict:
    """Get non-sensitive customer profile.

    FR-21: System MUST retrieve non-sensitive profile details (name, email, preferences).
    """
    return {
        "id": str(customer.id),
        "name": customer.name,
        "email": customer.email,
        "tier": customer.tier,
        "preferences": customer.preferences,
        "created_at": customer.created_at.isoformat() if customer.created_at else None,
        "updated_at": customer.updated_at.isoformat() if customer.updated_at else None,
    }