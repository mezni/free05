"""Order status transition use cases for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime

from domain.entities import Order, OrderStatus
from domain.policies import order_transition_allowed


def transition_to_processing(order: Order) -> Order:
    """Transition order to Processing status.

    FR-08: System MUST update order status through Processing → Completed → Returned/Cancelled.
    """
    return transition_order_status(order, OrderStatus.Processing)


def transition_to_completed(order: Order) -> Order:
    """Transition order to Completed status.

    FR-08: System MUST update order status through Processing → Completed → Returned/Cancelled.
    """
    return transition_order_status(order, OrderStatus.Completed)


def transition_to_returned(order: Order) -> Order:
    """Transition order to Returned status.

    FR-08: System MUST update order status through Processing → Completed → Returned/Cancelled.
    """
    return transition_order_status(order, OrderStatus.Returned)


def transition_to_cancelled(order: Order) -> Order:
    """Transition order to Cancelled status.

    FR-08: System MUST update order status through Processing → Completed → Returned/Cancelled.
    """
    return transition_order_status(order, OrderStatus.Cancelled)


def can_transition_to(
    order: Order,
    new_status: OrderStatus,
) -> bool:
    """Check if order can transition to a new status.

    FR-08: Validates status transitions.
    """
    return order_transition_allowed(order.status, new_status)