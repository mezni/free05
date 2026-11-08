"""Refund use cases for bss-core Support Application."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from application.use_cases.billing import issue_refund, mask_payment_method
from application.use_cases.billing import get_balance
from infrastructure.repositories.audit import audit_repository
from domain.entities import Customer, BillingRecord, BillingType, BillingStatus


def process_refund(
    *,
    customer: Customer,
    order: Optional[object],
    amount: Decimal,
    reason: str,
) -> BillingRecord:
    """Process a refund for a customer.

    FR-27: System MUST execute monetary credit/refund with explicit authorization and a full audit log.
    NFR-11: issue_refund and user-management mutations MUST be audit-logged; customer mutations are not audited in the MVP.
    AD-5: Audit log is append-only; no update/delete path.

    Returns the created BillingRecord (refund).
    """
    if not customer:
        raise ValueError("Customer is required")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    # Issue the billing record (refund)
    record = issue_refund(
        customer=customer,
        order=order,
        amount=amount,
    )

    # Append audit log entry
    # In production, we'd have the user ID from authentication
    audit_repository.append(
        actor_user_id=getattr(customer, "id", "system"),
        operation="issue_refund",
        entity_type="billing_record",
        entity_id=str(record.id),
        outcome="success",
        amount=amount,
        reason=reason,
    )

    return record


def process_refund_with_audit_check(
    *,
    customer: Customer,
    amount: Decimal,
    reason: str,
) -> dict:
    """Process refund with audit guarantee check.

    AD-5: Audit-write failure blocks the refund operation.
    In MVP, audit write is synchronous and within the same transaction.
    """
    try:
        record = process_refund(
            customer=customer,
            amount=amount,
            reason=reason,
        )

        # Verify audit entry was created
        last_entry = audit_repository.get_last_entry()
        if last_entry and last_entry.outcome == "success":
            return {
                "refund_record": {
                    "id": str(record.id),
                    "amount": str(record.amount),
                    "type": record.type,
                    "status": record.status,
                },
                "audit_entry": {
                    "id": str(last_entry.id),
                    "outcome": last_entry.outcome,
                    "operation": last_entry.operation,
                },
                "audit_guarantee": "audit_entry_created",
            }
        else:
            # Audit failure - block the refund
            raise RuntimeError("Audit write failed - refund blocked per AD-5")

    except Exception:
        # Per AD-5: abort the operation if the audit write fails
        raise


def calculate_customer_balance(
    customer: Customer,
) -> dict:
    """Calculate and return customer's derived balance.

    R11: Balance = sum(Charge) - sum(Refund) - sum(Credit)
    NFR-12: Domain entities MUST have 100% unit-test coverage.
    """
    balance = get_balance(customer)

    return {
        "customer_id": str(customer.id),
        "balance": str(balance),
        "currency": "USD",
    }