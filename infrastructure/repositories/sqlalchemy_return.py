"""SQLAlchemy return request repository implementing the ReturnRequestRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyReturnRequest
from domain.entities import ReturnRequest
from domain.ports.repositories import ReturnRequestRepositoryPort


class SqlAlchemyReturnRequestRepository(ReturnRequestRepositoryPort):
    """SQLAlchemy implementation of ReturnRequestRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, return_id: UUID) -> Optional[ReturnRequest]:
        stmt = select(SqlAlchemyReturnRequest).where(SqlAlchemyReturnRequest.id == str(return_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return ReturnRequest(
            id=UUID(row.id),
            order_item_id=UUID(row.order_item_id),
            rma_number=row.rma_number,
            reason=row.reason,
            quantity=row.quantity,
            status=row.status,
            shipping_label_url=row.shipping_label_url,
            created_at=row.created_at,
        )

    def get_by_order_item_id(self, order_item_id: UUID) -> List[ReturnRequest]:
        stmt = select(SqlAlchemyReturnRequest).where(SqlAlchemyReturnRequest.order_item_id == str(order_item_id))
        rows = self._session.scalars(stmt).all()
        return [
            ReturnRequest(
                id=UUID(row.id),
                order_item_id=UUID(row.order_item_id),
                rma_number=row.rma_number,
                reason=row.reason,
                quantity=row.quantity,
                status=row.status,
                shipping_label_url=row.shipping_label_url,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def get_by_rma_number(self, rma_number: str) -> Optional[ReturnRequest]:
        stmt = select(SqlAlchemyReturnRequest).where(SqlAlchemyReturnRequest.rma_number == rma_number)
        row = self._session.scalar(stmt)
        if not row:
            return None
        return ReturnRequest(
            id=UUID(row.id),
            order_item_id=UUID(row.order_item_id),
            rma_number=row.rma_number,
            reason=row.reason,
            quantity=row.quantity,
            status=row.status,
            shipping_label_url=row.shipping_label_url,
            created_at=row.created_at,
        )

    def create(self, return_request: ReturnRequest) -> ReturnRequest:
        db_return = SqlAlchemyReturnRequest(
            id=return_request.id,
            order_item_id=str(return_request.order_item_id),
            rma_number=return_request.rma_number,
            reason=return_request.reason,
            quantity=return_request.quantity,
            status=return_request.status,
            shipping_label_url=return_request.shipping_label_url,
            created_at=return_request.created_at,
        )
        self._session.add(db_return)
        self._session.flush()
        return ReturnRequest(
            id=UUID(db_return.id),
            order_item_id=UUID(db_return.order_item_id),
            rma_number=db_return.rma_number,
            reason=db_return.reason,
            quantity=db_return.quantity,
            status=db_return.status,
            shipping_label_url=db_return.shipping_label_url,
            created_at=db_return.created_at,
        )

    def update(self, return_request: ReturnRequest) -> ReturnRequest:
        stmt = select(SqlAlchemyReturnRequest).where(SqlAlchemyReturnRequest.id == return_request.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Return request {return_request.id} not found")
        row.status = return_request.status
        row.reason = return_request.reason
        self._session.flush()
        return ReturnRequest(
            id=UUID(row.id),
            order_item_id=UUID(row.order_item_id),
            rma_number=row.rma_number,
            reason=row.reason,
            quantity=row.quantity,
            status=row.status,
            shipping_label_url=row.shipping_label_url,
            created_at=row.created_at,
        )

    def delete(self, return_id: UUID) -> None:
        stmt = delete(SqlAlchemyReturnRequest).where(SqlAlchemyReturnRequest.id == str(return_id))
        self._session.execute(stmt)
        self._session.flush()