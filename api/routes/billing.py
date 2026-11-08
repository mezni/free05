"""Billing routes for bss-core Support Application API."""

from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Status
from application.use_cases.billing import (
    create_billing_record,
    list_billing_records,
    issue_refund,
    mask_payment_method,
    get_balance,
    mask_sensitive_data,
    format_currency_amount,
)
from application.use_cases.refunds import process_refund, process_refund_with_audit_check, calculate_customer_balance
from infrastructure.repositories.audit import audit_repository
from api.deps import get_current_user_with_scope
from domain.entities import Customer, BillingType, BillingStatus
from infrastructure.config import get_settings

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post(
    "",
    status_code=201,
    responses={400: {"description": "Validation error"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def create_billing_route(
    *,
    customer_id: str,
    order_id: Optional[str] = None,
    billing_type: BillingType = BillingType.Charge,
    amount: Decimal,
    currency: str = "USD",
    current_user: dict = Depends(get_current_user_with_scope(["Financial Write"])),
):
    """Create a billing record (charge, refund, or credit).

    FR-16: System MUST create billing records of type Charge, Refund, or Credit.
    FR-17: System MUST link billing records to customers (and orders where applicable).
    FR-19: System MUST store payment method masks only.
    """
    # Placeholder - actual customer lookup via repository
    from domain.entities import Customer
    customer = Customer(id=customer_id)  # Simplified

    try:
        record = create_billing_record(
            customer=customer,
            order=None if order_id is None else order_id,
            billing_type=billing_type,
            amount=amount,
            currency=currency,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(record.id),
        "customer_id": record.customer_id,
        "order_id": record.order_id,
        "type": record.type,
        "amount": str(record.amount),
        "currency": record.currency,
        "payment_method_mask": record.payment_method_mask,
        "status": record.status,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }


@router.get(
    "",
    response_model=List[dict],
    responses={401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def list_billing_route(
    *,
    customer_id: Optional[str] = None,
    billing_type: Optional[BillingType] = None,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """List billing records.

    FR-20: System MUST show billing history per customer.
    FR-24: System MUST return only masked payment data (PCI-DSS compliant).
    """
    records = list_billing_records(
        customer_id=customer_id,
        billing_type=billing_type,
    )

    return [
        {
            "id": str(r.id),
            "customer_id": r.customer_id,
            "order_id": r.order_id,
            "type": r.type,
            "amount": str(r.amount),
            "currency": r.currency,
            "payment_method_mask": r.payment_method_mask,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]


@router.post(
    "/refund",
    responses={
        400: {"description": "Validation error"},
        404: {"description": "Customer not found"},
        401: {"description": "Unauthenticated"},
        403: {"description": "Insufficient scope"},
    },
)
async def create_refund_route(
    *,
    customer_id: str,
    amount: Decimal,
    reason: str,
    current_user: dict = Depends(get_current_user_with_scope(["Financial Write"])),
):
    """Issue a refund to a customer.

    FR-27: System MUST execute monetary credit/refund with explicit authorization and a full audit log.
    AD-5: Audit log is append-only; audit failure blocks the refund operation.
    """
    # Placeholder - actual customer lookup via repository
    from domain.entities import Customer
    customer = Customer(id=customer_id)  # Simplified

    try:
        result = process_refund_with_audit_check(
            customer=customer,
            amount=amount,
            reason=reason,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {
        "refund_record": result["refund_record"],
        "audit_entry": result["audit_entry"],
        "audit_guarantee": result["audit_guarantee"],
    }


@router.get(
    "/balance/{customer_id}",
    responses={404: {"description": "Customer not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_balance_route(
    *,
    customer_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get customer derived balance.

    R11: Balance = sum(Charge) - sum(Refund) - sum(Credit).
    """
    # Placeholder - actual customer lookup via repository
    from domain.entities import Customer
    customer = Customer(id=customer_id)  # Simplified

    balance = calculate_customer_balance(customer)

    return {
        "customer_id": balance["customer_id"],
        "balance": balance["balance"],
        "currency": balance["currency"],
    }


@router.post(
    "/mask",
    responses={200: {"description": "Masked data"}, 400: {"description": "Invalid input"}},
)
async def mask_data_route(
    *,
    card_number: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Mask sensitive card data for PCI-DSS compliance.

    AD-4: Payment data must be masked at boundary; never store full PAN.
    FR-19: System MUST store payment method masks only.
    FR-24: System MUST return only masked payment data.
    """
    if not card_number:
        raise HTTPException(status_code=400, detail="Card number is required")

    masked = mask_sensitive_data(card_number)
    return {
        "original_length": len(card_number),
        "masked_data": masked,
    }