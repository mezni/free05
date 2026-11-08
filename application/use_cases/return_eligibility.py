"""Return eligibility use case for bss-core Support Application."""

from __future__ import annotations

from application.use_cases.orders import check_return_eligibility
from domain.services.eligibility import can_submit_return
from domain.entities import Order


def evaluate_return_eligibility(
    order: Order,
    *,
    days: int = 30,
) -> dict:
    """Evaluate return eligibility for an order.

    FR-09: System MUST mark items as eligible or non-eligible for return.
    FR-25: System MUST evaluate return windows and policy to decide refund eligibility deterministically.

    Returns eligibility decision with per-item details.
    """
    if not order:
        raise ValueError("Order is required")

    eligibility = check_return_eligibility(order, days=days)

    return {
        "order_id": eligibility["order_id"],
        "return_window_days": eligibility["return_window_days"],
        "overall_eligible": eligibility["eligible"],
        "eligible_items": [
            item for item in eligibility["items"] if item["eligible"]
        ],
        "ineligible_items": [
            item for item in eligibility["items"] if not item["eligible"]
        ],
        "reason": (
            "All items within return window"
            if eligibility["eligible"]
            else "Some items outside return window"
        ),
    }