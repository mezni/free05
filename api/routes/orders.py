"""Order and return routes for bss-core Support Application API."""

from __future__ import annotations

from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from application.use_cases.orders import (
    create_order,
    add_order_item,
    remove_order_item,
    transition_order_status,
    check_return_eligibility,
    get_return_label_info,
)
from application.use_cases.order_status import (
    transition_to_processing,
    transition_to_completed,
    transition_to_returned,
    transition_to_cancelled,
    can_transition_to,
)
from application.use_cases.returns import create_return_request, submit_return, process_idempotent_return
from api.deps import get_current_user_with_scope
from domain.entities import Customer, Order, OrderStatus, ReturnStatus

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "",
    status_code=201,
    responses={400: {"description": "Validation error"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def create_order_route(
    *,
    customer_id: str,
    items: list[dict],
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Create a new order.

    FR-06: System MUST create orders associated with a customer.
    FR-07: System MUST add and remove order items (product, quantity, price).
    FR-10: System MUST calculate the order total from its items.
    """
    # Placeholder - actual customer lookup via repository
    from domain.entities import Customer
    customer = Customer(id=customer_id)  # Simplified

    try:
        order = create_order(customer=customer, items=items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(order.id),
        "customer_id": order.customer_id,
        "status": order.status,
        "total_amount": str(order.total_amount),
        "currency": order.currency,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }


@router.post(
    "/{order_id}/items",
    responses={400: {"description": "Validation error"}, 404: {"description": "Order not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def add_item_route(
    *,
    order_id: str,
    product_id: str,
    quantity: int,
    unit_price: Decimal,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Add an item to an order.

    FR-07: System MUST add and remove order items (product, quantity, price).
    """
    # Placeholder - actual order lookup via repository
    from domain.entities import Order
    order = Order(id=order_id)  # Simplified

    try:
        order = add_order_item(
            order,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(order.id),
        "status": order.status,
        "total_amount": str(order.total_amount),
        "items_count": len(order.items),
    }


@router.post(
    "/{order_id}/items/remove",
    responses={400: {"description": "Validation error"}, 404: {"description": "Order not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def remove_item_route(
    *,
    order_id: str,
    product_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Remove an item from an order.

    FR-07: System MUST add and remove order items (product, quantity, price).
    """
    # Placeholder - actual order lookup via repository
    from domain.entities import Order
    order = Order(id=order_id)  # Simplified

    try:
        order = remove_order_item(order, product_id=product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(order.id),
        "status": order.status,
        "total_amount": str(order.total_amount),
        "items_count": len(order.items),
    }


@router.post(
    "/{order_id}/status",
    responses={
        400: {"description": "Invalid transition"},
        404: {"description": "Order not found"},
        401: {"description": "Unauthenticated"},
        403: {"description": "Insufficient scope"},
    },
)
async def transition_status_route(
    *,
    order_id: str,
    new_status: OrderStatus,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Transition order status.

    FR-08: System MUST update order status through Processing → Completed → Returned/Cancelled.
    """
    # Placeholder - actual order lookup via repository
    from domain.entities import Order
    order = Order(id=order_id)  # Simplified

    try:
        order = transition_order_status(order, new_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(order.id),
        "status": order.status,
    }


@router.get(
    "/{order_id}/eligibility",
    responses={404: {"description": "Order not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def check_eligibility_route(
    *,
    order_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Check return eligibility for an order.

    FR-09: System MUST mark items as eligible or non-eligible for return.
    FR-25: System MUST evaluate return windows and policy to decide refund eligibility deterministically.
    """
    # Placeholder - actual order lookup via repository
    from domain.entities import Order
    order = Order(id=order_id)  # Simplified

    eligibility = check_return_eligibility(order)
    return {
        "order_id": eligibility["order_id"],
        "eligible": eligibility["eligible"],
        "items": eligibility["items"],
    }


@router.post(
    "/{order_id}/return",
    responses={
        400: {"description": "Invalid return request"},
        404: {"description": "Order not found"},
        401: {"description": "Unauthenticated"},
        403: {"description": "Insufficient scope"},
    },
)
async def submit_return_route(
    *,
    order_id: str,
    reason: str,
    idempotency_key: str,
    quantity: int = 1,
    current_user: dict = Depends(get_current_user_with_scope(["Financial Write"])),
):
    """Submit a return request.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    # Placeholder - actual order item lookup via repository
    from domain.entities import OrderItem
    order_item = OrderItem(id=order_id)  # Simplified

    try:
        return_request = submit_return(
            order_item_id=order_item.id,
            idempotency_key=idempotency_key,
            reason=reason,
            quantity=quantity,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(return_request.id),
        "rma_number": return_request.rma_number,
        "idempotency_key": return_request.idempotency_key,
        "status": return_request.status,
        "shipping_label_url": return_request.shipping_label_url,
    }


@router.get(
    "/{order_id}/return-label",
    responses={404: {"description": "Return not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_return_label_route(
    *,
    order_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get return shipping label URL.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    # Placeholder - actual return request lookup via repository
    from application.use_cases.returns import process_idempotent_return
    return_request = process_idempotent_return(order_id)

    if not return_request:
        raise HTTPException(status_code=404, detail="Return not found")

    return {
        "rma_number": return_request.rma_number,
        "shipping_label_url": return_request.shipping_label_url,
    }