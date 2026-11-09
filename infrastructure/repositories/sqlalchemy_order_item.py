"""SQLAlchemy order item repository implementing the OrderItemRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyOrderItem
from domain.entities import OrderItem
from domain.ports.repositories import OrderItemRepositoryPort


class SqlAlchemyOrderItemRepository(OrderItemRepositoryPort):
    """SQLAlchemy implementation of OrderItemRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: UUID) -> Optional[OrderItem]:
        stmt = select(SqlAlchemyOrderItem).where(SqlAlchemyOrderItem.id == str(item_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return OrderItem(
            id=UUID(row.id),
            order_id=UUID(row.order_id),
            product_id=UUID(row.product_id),
            quantity=row.quantity,
            unit_price=Decimal(row.unit_price),
            line_total=Decimal(row.line_total),
        )

    def get_by_order_id(self, order_id: UUID) -> List[OrderItem]:
        stmt = select(SqlAlchemyOrderItem).where(SqlAlchemyOrderItem.order_id == str(order_id))
        rows = self._session.scalars(stmt).all()
        return [
            OrderItem(
                id=UUID(row.id),
                order_id=UUID(row.order_id),
                product_id=UUID(row.product_id),
                quantity=row.quantity,
                unit_price=Decimal(row.unit_price),
                line_total=Decimal(row.line_total),
            )
            for row in rows
        ]

    def create(self, item: OrderItem) -> OrderItem:
        db_item = SqlAlchemyOrderItem(
            id=item.id,
            order_id=item.order_id,
            product_id=str(item.product_id),
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.line_total,
        )
        self._session.add(db_item)
        self._session.flush()
        return OrderItem(
            id=UUID(db_item.id),
            order_id=UUID(db_item.order_id),
            product_id=UUID(db_item.product_id),
            quantity=db_item.quantity,
            unit_price=db_item.unit_price,
            line_total=db_item.line_total,
        )

    def update(self, item: OrderItem) -> OrderItem:
        stmt = select(SqlAlchemyOrderItem).where(SqlAlchemyOrderItem.id == item.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Order item {item.id} not found")
        row.quantity = item.quantity
        row.unit_price = item.unit_price
        row.line_total = item.line_total
        self._session.flush()
        return OrderItem(
            id=UUID(row.id),
            order_id=UUID(row.order_id),
            product_id=UUID(row.product_id),
            quantity=row.quantity,
            unit_price=Decimal(row.unit_price),
            line_total=Decimal(row.line_total),
        )

    def delete(self, item_id: UUID) -> None:
        stmt = delete(SqlAlchemyOrderItem).where(SqlAlchemyOrderItem.id == str(item_id))
        self._session.execute(stmt)
        self._session.flush()