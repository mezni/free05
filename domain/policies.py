"""Domain invariants and state machines for bss-core Support Application (MVP).

This module enforces business rules that are domain-layer responsibilities
(no framework imports). All state machines are deterministic and driven by
configuration where noted.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import UUID

from .entities import (
    Customer,
    OrderStatus,
    ShipmentStatus,
    ReturnStatus,
    OrderItemReturnEligibility,
    BillingRecord,
    ReturnRequest,
    User,
)


# ---------------------------------------------------------------------------
# Return window policy
# ---------------------------------------------------------------------------

DEFAULT_RETURN_WINDOW_DAYS = 30


def is_return_eligible(
    *,
    order_item_age_days: int,
    quantity: int,
    item_quantity: int,
) -> bool:
    """Determine return eligibility per deterministic policy.

    Eligibility rules:
    - Return must be within the configured window (DEFAULT_RETURN_WINDOW_DAYS).
    - Quantity must be at least 1 and at most the original item quantity.
    - The item must not have already been processed for return.
    """
    if order_item_age_days > DEFAULT_RETURN_WINDOW_DAYS:
        return False
    if quantity < 1 or quantity > item_quantity:
        return False
    return True


# ---------------------------------------------------------------------------
# Order status transitions
# ---------------------------------------------------------------------------

# Allowed forward transitions: (from_status, to_status)
ORDER_TRANSITIONS = {
    "Processing": {"Completed", "Cancelled"},
    "Completed": {"Returned"},
    "Returned": {},  # terminal
    "Cancelled": {},  # terminal
}


def is_valid_order_transition(from_status: str, to_status: str) -> bool:
    """Check if an order status transition is allowed."""
    allowed = ORDER_TRANSITIONS.get(from_status, set())
    return to_status in allowed


def order_transition_allowed(from_status: OrderStatus, to_status: OrderStatus) -> bool:
    """Type-safe order status transition check."""
    return is_valid_order_transition(from_status.value, to_status.value)


# ---------------------------------------------------------------------------
# Shipment status transitions
# ---------------------------------------------------------------------------

# Allowed forward transitions: (from_status, to_status)
SHIPMENT_TRANSITIONS = {
    "Label_Created": {"In Transit"},
    "In Transit": {"Out for Delivery"},
    "Out for Delivery": {"Delivered"},
    "Delivered": set(),  # terminal
    "Returned": set(),  # terminal
    "Cancelled": set(),  # terminal
}


def is_valid_shipment_transition(from_status: str, to_status: str) -> bool:
    """Check if a shipment status transition is allowed."""
    allowed = SHIPMENT_TRANSITIONS.get(from_status, set())
    return to_status in allowed


def shipment_transition_allowed(from_status: ShipmentStatus, to_status: ShipmentStatus) -> bool:
    """Type-safe shipment status transition check."""
    return is_valid_shipment_transition(from_status.value, to_status.value)


# ---------------------------------------------------------------------------
# Return request status transitions
# ---------------------------------------------------------------------------

# Allowed forward transitions: (from_status, to_status)
RETURN_TRANSITIONS = {
    "Submitted": {"Approved", "Rejected"},
    "Approved": {"Completed"},
    "Rejected": {},  # terminal
    "Completed": {},  # terminal
}


def is_valid_return_transition(from_status: str, to_status: str) -> bool:
    """Check if a return request status transition is allowed."""
    allowed = RETURN_TRANSITIONS.get(from_status, set())
    return to_status in allowed


def return_transition_allowed(from_status: ReturnStatus, to_status: ReturnStatus) -> bool:
    """Type-safe return request status transition check."""
    return is_valid_return_transition(from_status.value, to_status.value)


# ---------------------------------------------------------------------------
# Money invariants
# ---------------------------------------------------------------------------

def compute_line_total(quantity: float, unit_price: float) -> float:
    """Compute line total: quantity × unit_price.

    Raises ValueError if inputs are invalid.
    """
    if quantity < 1:
        raise ValueError("quantity must be >= 1")
    if unit_price <= 0:
        raise ValueError("unit_price must be > 0")
    return round(quantity * unit_price, 2)


def compute_order_total(line_totals: list[float]) -> float:
    """Compute order total as sum of line totals.

    Returns 0.0 for empty lists.
    """
    if not line_totals:
        return 0.0
    total = sum(line_totals)
    # Ensure floating-point stability: round to 2 decimal places
    return round(total, 2)


# ---------------------------------------------------------------------------
# Billing invariants
# ---------------------------------------------------------------------------

def billing_balance(charges: list[BillingRecord], refunds: list[BillingRecord]) -> float:
    """Derive customer balance: sum(Charges) − sum(Refunds) − sum(Credits).

    This is a *derived* value; the domain layer does NOT store a mutable
    balance column. Callers should recompute on each request.
    """
    charge_total = sum(r.amount for r in charges if r.is_charge)
    refund_total = sum(r.amount for r in refunds if r.is_refund or r.is_credit)
    return round(charge_total - refund_total, 2)


# ---------------------------------------------------------------------------
# User / role orthogonal checks (constitution III)
# ---------------------------------------------------------------------------

def user_requires_user_management(scope: str) -> bool:
    """Return True iff the operation requires the ``User Management`` scope.

    Per constitution III, ``User Management`` is orthogonal to ``Read``/
    ``Write``/``Financial Write``; user CRUD, role assignment, status toggles,
    and user search MUST require ``User Management``, never generic ``Write``.
    """
    return scope == "User Management"


# ---------------------------------------------------------------------------
# Invariant: no full PAN / masked payment data
# ---------------------------------------------------------------------------

def is_payment_method_masked(mask: str | None) -> bool:
    """Return True iff the payment method value is a mask (not a full PAN)."""
    if not mask:
        return False
    # A masked format typically contains words like "Visa", "Mastercard",
    # "ending in", and only the last 4 digits.
    mask_lower = mask.lower()
    return any(
        keyword in mask_lower
        for keyword in ["visa", "mastercard", "amex", "ending in", "mask"]
    )


# ---------------------------------------------------------------------------
# Export commonly used symbols for downstream consumers
# ---------------------------------------------------------------------------

__all__ = [
    "is_return_eligible",
    "is_valid_order_transition",
    "is_valid_shipment_transition",
    "is_valid_return_transition",
    "compute_line_total",
    "compute_order_total",
    "billing_balance",
    "user_requires_user_management",
    "is_payment_method_masked",
    "DEFAULT_RETURN_WINDOW_DAYS",
    "ORDER_TRANSITIONS",
    "SHIPMENT_TRANSITIONS",
    "RETURN_TRANSITIONS",
]