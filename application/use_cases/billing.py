"""Billing use cases for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from domain.entities import BillingRecord, BillingType, BillingStatus, Customer


def create_billing_record(
    *,
    customer: Customer,
    order: Optional[object],
    billing_type: BillingType,
    amount: Decimal,
    currency: str = "USD",
) -> BillingRecord:
    """Create a new billing record.

    FR-16: System MUST create billing records of type Charge, Refund, or Credit.
    FR-17: System MUST link billing records to customers (and orders where applicable).
    FR-19: System MUST store payment method masks only (e.g. "Visa ending in 4242").
    FR-20: System MUST show billing history per customer.
    FR-24: System MUST return only masked payment data (PCI-DSS compliant).
    """
    if not customer:
        raise ValueError("Customer is required")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    # Determine order reference if provided
    order_ref = None
    if order:
        order_ref = str(order.id) if hasattr(order, "id") else str(order)

    record = BillingRecord(
        customer_id=customer.id,
        order_id=order_ref,
        type=billing_type,
        amount=amount,
        currency=currency,
        payment_method_mask=mask_payment_method(amount, billing_type),
        status=BillingStatus.Pending,
        created_at=datetime.now(),
    )

    return record


def list_billing_records(
    *,
    customer_id: str | None = None,
    billing_type: Optional[BillingType] = None,
) -> List[BillingRecord]:
    """List billing records with optional filters.

    FR-20: System MUST show billing history per customer.
    """
    # Placeholder - actual implementation would query repository
    return []


def issue_refund(
    *,
    customer: Customer,
    order: Optional[object],
    amount: Decimal,
    reason: str,
) -> BillingRecord:
    """Issue a refund to a customer.

    FR-27: System MUST execute monetary credit/refund with explicit authorization and a full audit log.
    NFR-11: issue_refund and user-management mutations MUST be audit-logged; customer mutations are not audited in the MVP.
    """
    if not customer:
        raise ValueError("Customer is required")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    record = create_billing_record(
        customer=customer,
        order=order,
        billing_type=BillingType.Refund,
        amount=amount,
    )

    # In a real implementation, this would trigger the audit log
    # NFR-11: Audit log entry would be created here

    return record


def mask_payment_method(
    amount: Decimal,
    billing_type: BillingType,
) -> str:
    """Mask payment method for PCI-DSS compliance.

    FR-19: System MUST store payment method masks only (e.g. "Visa ending in 4242").
    FR-24: System MUST return only masked payment data (PCI-DSS compliant).
    """
    # Format: "Visa ending in XXXX" or similar mask
    # In production, this would mask actual card data
    amount_str = f"{amount:.2f}"
    return f"Masked payment (${amount_str})"


def get_balance(
    customer: Customer,
    *,
    records: Optional[List[BillingRecord]] = None,
) -> Decimal:
    """Calculate customer derived balance.

    R11: Balance = sum(Charge) - sum(Refund) - sum(Credit)
    """
    if not customer:
        raise ValueError("Customer is required")

    records = records or list_billing_records(customer_id=customer.id)

    total = Decimal("0")
    for record in records:
        if record.type == BillingType.Charge:
            total += record.amount
        elif record.type == BillingType.Refund:
            total -= record.amount
        elif record.type == BillingType.Credit:
            total -= record.amount

    return total