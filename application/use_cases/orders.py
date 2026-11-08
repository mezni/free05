"""Order use cases for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from domain.entities import (
    Customer,
    Order,
    OrderItem,
    OrderStatus,
    ShipmentStatus,
    ReturnStatus,
    Product,
    Inventory,
)
from domain.services.eligibility import is_item_in_return_window


def create_order(
    *,
    customer: Customer,
    items: list[dict],
) -> Order:
    """Create a new order for a customer.

    FR-06: System MUST create orders associated with a customer.
    FR-07: System MUST add and remove order items (product, quantity, price).
    FR-10: System MUST calculate the order total from its items.

    Each item dict must have: product_id, quantity, unit_price
    """
    if not customer:
        raise ValueError("Customer is required")
    if not items:
        raise ValueError("At least one item is required")

    order_items: list[OrderItem] = []
    total = Decimal("0")

    for item_data in items:
        product_id = item_data.get("product_id")
        quantity = item_data.get("quantity", 1)
        unit_price = Decimal(str(item_data.get("unit_price", "0")))

        if not product_id:
            raise ValueError("Product ID is required")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        if unit_price <= 0:
            raise ValueError("Unit price must be greater than 0")

        # Calculate line total
        line_total = quantity * unit_price
        total += line_total

        order_item = OrderItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total,
            return_eligible=True,  # Default; actual eligibility checked later
        )
        order_items.append(order_item)

    order = Order(
        customer_id=customer.id,
        status=OrderStatus.Processing,
        items=order_items,
        total_amount=total,
        currency="USD",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Update order total from items
    order.total_amount = calculate_order_total(order)

    return order


def add_order_item(
    order: Order,
    *,
    product_id: str,
    quantity: int,
    unit_price: Decimal,
) -> Order:
    """Add an item to an existing order.

    FR-07: System MUST add and remove order items (product, quantity, price).
    """
    if not order:
        raise ValueError("Order is required")
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    if unit_price <= 0:
        raise ValueError("Unit price must be greater than 0")

    line_total = quantity * unit_price
    new_item = OrderItem(
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        line_total=line_total,
        return_eligible=True,
    )
    order.items.append(new_item)
    order.total_amount = calculate_order_total(order)
    order.updated_at = datetime.now()

    return order


def remove_order_item(
    order: Order,
    *,
    product_id: str,
) -> Order:
    """Remove an item from an existing order.

    FR-07: System MUST add and remove order items (product, quantity, price).
    """
    if not order:
        raise ValueError("Order is required")

    order.items = [item for item in order.items if item.product_id != product_id]
    order.total_amount = calculate_order_total(order)
    order.updated_at = datetime.now()

    return order


def transition_order_status(
    order: Order,
    new_status: OrderStatus,
) -> Order:
    """Transition order status.

    FR-08: System MUST update order status through Processing → Completed → Returned/Cancelled.
    Invalid transitions raise domain error → API maps to 409.
    """
    if not order:
        raise ValueError("Order is required")

    if not order_transition_allowed(order.status, new_status):
        raise ValueError(
            f"Invalid status transition from {order.status} to {new_status}"
        )

    order.status = new_status
    order.updated_at = datetime.now()

    return order


def check_return_eligibility(
    order: Order,
    *,
    days: int | None = None,
) -> dict:
    """Check if items in an order are eligible for return.

    FR-09: System MUST mark items as eligible or non-eligible for return.
    FR-25: System MUST evaluate return windows and policy to decide refund eligibility deterministically.

    Returns dict with per-item eligibility and reasons.
    """
    if not order:
        raise ValueError("Order is required")

    days = days or 30  # default return window

    eligibility_results = []
    for item in order.items:
        eligible, reason = is_item_in_return_window(item, days=days)
        eligibility_results.append(
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "eligible": eligible,
                "reason": reason,
            }
        )

    return {
        "order_id": str(order.id),
        "eligible": all(e["eligible"] for e in eligibility_results),
        "items": eligibility_results,
    }


def get_return_label_info(
    order_item: OrderItem,
) -> dict:
    """Get return label information for an order item.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    if not order_item:
        raise ValueError("Order item is required")

    return {
        "rma_number": f"RMA-{order_item.id}",
        "shipping_label_url": f"/labels/{order_item.id}",
        "eligible": order_item.return_eligible,
    }