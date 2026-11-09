"""SQLAlchemy billing record repository implementing the BillingRecordRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyBillingRecord
from domain.entities import BillingRecord
from domain.ports.repositories import BillingRecordRepositoryPort


class SqlAlchemyBillingRecordRepository(BillingRecordRepositoryPort):
    """SQLAlchemy implementation of BillingRecordRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, billing_id: UUID) -> Optional[BillingRecord]:
        stmt = select(SqlAlchemyBillingRecord).where(SqlAlchemyBillingRecord.id == str(billing_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return BillingRecord(
            id=UUID(row.id),
            customer_id=UUID(row.customer_id),
            order_id=UUID(row.order_id) if row.order_id else None,
            type=row.type,
            amount=Decimal(row.amount),
            currency=row.currency,
            status=row.status,
            payment_method_mask=row.payment_method_mask,
            created_at=row.created_at,
        )

    def get_by_customer_id(self, customer_id: UUID) -> List[BillingRecord]:
        stmt = select(SqlAlchemyBillingRecord).where(SqlAlchemyBillingRecord.customer_id == str(customer_id))
        rows = self._session.scalars(stmt).all()
        return [
            BillingRecord(
                id=UUID(row.id),
                customer_id=UUID(row.customer_id),
                order_id=UUID(row.order_id) if row.order_id else None,
                type=row.type,
                amount=Decimal(row.amount),
                currency=row.currency,
                status=row.status,
                payment_method_mask=row.payment_method_mask,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def get_by_order_id(self, order_id: UUID) -> Optional[BillingRecord]:
        stmt = select(SqlAlchemyBillingRecord).where(SqlAlchemyBillingRecord.order_id == str(order_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return BillingRecord(
            id=UUID(row.id),
            customer_id=UUID(row.customer_id),
            order_id=UUID(row.order_id),
            type=row.type,
            amount=Decimal(row.amount),
            currency=row.currency,
            status=row.status,
            payment_method_mask=row.payment_method_mask,
            created_at=row.created_at,
        )

    def create(self, billing: BillingRecord) -> BillingRecord:
        db_billing = SqlAlchemyBillingRecord(
            id=billing.id,
            customer_id=str(billing.customer_id),
            order_id=str(billing.order_id) if billing.order_id else None,
            type=billing.type,
            amount=billing.amount,
            currency=billing.currency,
            status=billing.status,
            payment_method_mask=billing.payment_method_mask,
            created_at=billing.created_at,
        )
        self._session.add(db_billing)
        self._session.flush()
        return BillingRecord(
            id=UUID(db_billing.id),
            customer_id=UUID(db_billing.customer_id),
            order_id=UUID(db_billing.order_id) if db_billing.order_id else None,
            type=db_billing.type,
            amount=db_billing.amount,
            currency=db_billing.currency,
            status=db_billing.status,
            payment_method_mask=db_billing.payment_method_mask,
            created_at=db_billing.created_at,
        )

    def update(self, billing: BillingRecord) -> BillingRecord:
        stmt = select(SqlAlchemyBillingRecord).where(SqlAlchemyBillingRecord.id == billing.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Billing record {billing.id} not found")
        row.type = billing.type
        row.amount = billing.amount
        row.currency = billing.currency
        row.status = billing.status
        row.payment_method_mask = billing.payment_method_mask
        self._session.flush()
        return BillingRecord(
            id=UUID(row.id),
            customer_id=UUID(row.customer_id),
            order_id=UUID(row.order_id) if row.order_id else None,
            type=row.type,
            amount=Decimal(row.amount),
            currency=row.currency,
            status=row.status,
            payment_method_mask=row.payment_method_mask,
            created_at=row.created_at,
        )

    def delete(self, billing_id: UUID) -> None:
        stmt = delete(SqlAlchemyBillingRecord).where(SqlAlchemyBillingRecord.id == str(billing_id))
        self._session.execute(stmt)
        self._session.flush()