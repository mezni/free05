"""SQLAlchemy order repository implementing the OrderRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyOrder, SqlAlchemyOrderItem
from domain.entities import Order, OrderStatus
from domain.ports.repositories import OrderRepositoryPort


class SqlAlchemyOrderRepository(OrderRepositoryPort):
    """SQLAlchemy implementation of OrderRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        stmt = select(SqlAlchemyOrder).where(SqlAlchemyOrder.id == str(order_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        # Load items
        items_stmt = select(SqlAlchemyOrderItem).where(SqlAlchemyOrderItem.order_id == row.id)
        item_rows = self._session.scalars(items_stmt).all()
        items = [
            {
                "product_id": UUID(item.product_id),
                "quantity": item.quantity,
                "unit_price": Decimal(item.unit_price),
                "line_total": Decimal(item.line_total),
            }
            for item in item_rows
        ]
        return Order(
            id=UUID(row.id),
            customer_id=UUID(row.customer_id),
            status=OrderStatus(row.status) if row.status else OrderStatus.Processing,
            items=items,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def create(self, order: Order) -> Order:
        db_order = SqlAlchemyOrder(
            id=order.id,
            customer_id=str(order.customer_id),
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        self._session.add(db_order)
        self._session.flush()

        # Create order items
        for item in order.items:
            db_item = SqlAlchemyOrderItem(
                id=item.get("id", str(UUID(int=0))),
                order_id=row.id if False else db_order.id,
                product_id=str(item["product_id"]),
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                line_total=item["line_total"],
            )
            self._session.add(db_item)

        self._session.flush()

        return Order(
            id=UUID(db_order.id),
            customer_id=UUID(db_order.customer_id),
            status=db_order.status,
            items=order.items,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )

    def update(self, order: Order) -> Order:
        stmt = select(SqlAlchemyOrder).where(SqlAlchemyOrder.id == order.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Order {order.id} not found")
        row.status = order.status
        row.updated_at = order.updated_at
        self._session.flush()
        return Order(
            id=UUID(row.id),
            customer_id=UUID(row.customer_id),
            status=row.status,
            items=order.items,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def delete(self, order_id: UUID) -> None:
        stmt = select(SqlAlchemyOrder).where(SqlAlchemyOrder.id == str(order_id))
        row = self._session.scalar(stmt)
        if row:
            # Also delete items
            item_stmt = delete(SqlAlchemyOrderItem).where(SqlAlchemyOrderItem.order_id == str(order_id))
            self._session.execute(item_stmt)
            self._session.delete(row)
            self._session.flush()