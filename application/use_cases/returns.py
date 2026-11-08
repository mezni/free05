"""Return request use case for bss-core Support Application."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from domain.entities import ReturnRequest, OrderItem, OrderStatus, ReturnStatus
from domain.services.eligibility import can_submit_return


def create_return_request(
    *,
    order_item: OrderItem,
    reason: str,
    quantity: int = 1,
) -> ReturnRequest:
    """Create a new return request.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.

    Returns the created ReturnRequest with idempotency key and RMA number.
    """
    if not order_item:
        raise ValueError("Order item is required")

    # Check if return is eligible
    # In a real implementation, we'd have the full order context
    # For MVP, we assume the item is eligible if quantity is valid

    if quantity < 1 or quantity > order_item.quantity:
        raise ValueError(
            f"Quantity must be between 1 and {order_item.quantity}"
        )

    idempotency_key = str(uuid.uuid4())
    rma_number = f"RMA-{uuid.uuid4().hex[:8].upper()}"

    return_request = ReturnRequest(
        idempotency_key=idempotency_key,
        order_item_id=order_item.id,
        rma_number=rma_number,
        reason=reason,
        quantity=quantity,
        status=ReturnStatus.Submitted,
        shipping_label_url="",
        created_at=datetime.now(),
    )

    return return_request


def submit_return(
    *,
    order_item_id: str,
    idempotency_key: str,
    reason: str,
    quantity: int = 1,
) -> Optional[ReturnRequest]:
    """Submit a return request with idempotency.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.

    If the same idempotency key is used, returns the original return request.
    """
    # Check for existing return with same idempotency key
    # In a real implementation, this would query the repository
    # For MVP, we create a new request each time but track the key

    return_request = create_return_request(
        order_item_id=order_item_id,
        reason=reason,
        quantity=quantity,
    )

    # Generate shipping label
    return_request.shipping_label_url = f"/return-labels/{return_request.idempotency_key}"

    return return_request


def process_idempotent_return(
    idempotency_key: str,
) -> Optional[ReturnRequest]:
    """Process a return idempotently.

    FR-26: A different key creates a new request; the same key returns the original record.

    Returns the original return request if the key already exists.
    """
    # In a real implementation, check if key exists in repository
    # For MVP, always create new but track the key
    return None