"""Return routes for bss-core Support Application API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Status
from typing import Optional

from application.use_cases.returns import create_return_request, submit_return, process_idempotent_return
from api.deps import get_current_user_with_scope
from domain.entities import ReturnRequest, ReturnStatus

router = APIRouter(prefix="/returns", tags=["returns"])


@router.post(
    "",
    status_code=201,
    responses={400: {"description": "Validation error"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def create_return_route(
    *,
    order_item_id: str,
    reason: str,
    idempotency_key: str,
    quantity: int = 1,
    current_user: dict = Depends(get_current_user_with_scope(["Financial Write"])),
):
    """Create a return request.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    try:
        return_request = create_return_request(
            order_item_id=order_item_id,
            reason=reason,
            idempotency_key=idempotency_key,
            quantity=quantity,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(return_request.id),
        "rma_number": return_request.rma_number,
        "idempotency_key": return_request.idempotency_key,
        "status": return_request.status,
    }


@router.post(
    "/submit",
    responses={400: {"description": "Validation error"}, 404: {"description": "Order/item not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def submit_return_route(
    *,
    order_item_id: str,
    idempotency_key: str,
    reason: str,
    quantity: int = 1,
    current_user: dict = Depends(get_current_user_with_scope(["Financial Write"])),
):
    """Submit a return request.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    try:
        return_request = submit_return(
            order_item_id=order_item_id,
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
    "/{return_id}",
    responses={404: {"description": "Return not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_return_route(
    *,
    return_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get return request by ID.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    # Placeholder - actual lookup via repository
    raise HTTPException(status_code=404, detail="Return not found")


@router.get(
    "/{return_id}/label",
    responses={404: {"description": "Return not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_return_label_route(
    *,
    return_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get return shipping label URL.

    FR-26: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.
    """
    # Placeholder - actual return request lookup via repository
    from application.use_cases.returns import process_idempotent_return
    return_request = process_idempotent_return(return_id)

    if not return_request:
        raise HTTPException(status_code=404, detail="Return not found")

    return {
        "rma_number": return_request.rma_number,
        "shipping_label_url": return_request.shipping_label_url,
    }