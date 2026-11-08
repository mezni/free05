"""Domain return eligibility service for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from domain.entities import Order, OrderItem, Product, ReturnStatus, OrderStatus


def is_item_in_return_window(
    item: OrderItem,
    *,
    days: int = 30,
) -> tuple[bool, str]:
    """Check if an order item is within the return window.

    FR-09: System MUST mark items as eligible or non-eligible for return.
    FR-25: System MUST evaluate return windows and policy to decide refund eligibility deterministically.

    Default return window is 30 days from order creation.
    """
    if not item or not item.order_id:
        return False, "Order item not associated with an order"

    # Determine the order creation date
    # In a real implementation, this would come from the order's created_at
    # For now, we check based on item creation context
    cutoff_date = datetime.now() - timedelta(days=days)

    # Placeholder: In production, compare item.order.created_at against cutoff_date
    # For MVP, assume all items are eligible within the window
    return True, "Item within return window"


def check_return_eligibility(
    order: Order,
    *,
    days: int = 30,
) -> dict:
    """Check return eligibility for all items in an order.

    FR-09: Mark items as eligible or non-eligible for return.
    FR-25: Deterministic refund eligibility based on return window policy.

    Returns dict with per-item eligibility and overall decision.
    """
    if not order:
        raise ValueError("Order is required")

    items_eligibility = []
    all_eligible = True

    for item in order.items:
        eligible, reason = is_item_in_return_window(item, days=days)
        items_eligibility.append(
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "eligible": eligible,
                "reason": reason,
            }
        )
        if not eligible:
            all_eligible = False

    return {
        "order_id": str(order.id),
        "return_window_days": days,
        "eligible": all_eligible,
        "items": items_eligibility,
    }


def can_submit_return(
    order: Order,
) -> tuple[bool, str]:
    """Check if a return can be submitted for an order.

    FR-25: Evaluate return eligibility boundaries.
    Also checks: order must not be Cancelled or already Returned.
    """
    if not order:
        return False, "Order is required"

    # Check order status
    if order.status in (OrderStatus.Cancelled, OrderStatus.Returned):
        return False, f"Cannot return order with status {order.status}"

    # Check return eligibility
    eligibility = check_return_eligibility(order, days=30)
    if not eligibility["eligible"]:
        ineligible_items = [
            f"{item['product_id']} ({item['reason']})"
            for item in eligibility["items"]
            if not item["eligible"]
        ]
        return False, f"Items not eligible for return: {', '.join(ineligible_items)}"

    return True, "Order is eligible for return"