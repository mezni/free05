"""SQLAlchemy inventory repository implementing the InventoryRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyInventory
from domain.entities import Inventory
from domain.ports.repositories import InventoryRepositoryPort


class SqlAlchemyInventoryRepository(InventoryRepositoryPort):
    """SQLAlchemy implementation of InventoryRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_product_id(self, product_id: UUID) -> Optional[Inventory]:
        stmt = select(SqlAlchemyInventory).where(SqlAlchemyInventory.product_id == str(product_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Inventory(
            product_id=UUID(row.product_id),
            stock_quantity=row.stock_quantity,
            low_stock_threshold=row.low_stock_threshold,
            last_updated=row.last_updated,
        )

    def create(self, inventory: Inventory) -> Inventory:
        db_inventory = SqlAlchemyInventory(
            product_id=inventory.product_id,
            stock_quantity=inventory.stock_quantity,
            low_stock_threshold=inventory.low_stock_threshold,
            last_updated=inventory.last_updated,
        )
        self._session.add(db_inventory)
        self._session.flush()
        return Inventory(
            product_id=UUID(db_inventory.product_id),
            stock_quantity=db_inventory.stock_quantity,
            low_stock_threshold=db_inventory.low_stock_threshold,
            last_updated=db_inventory.last_updated,
        )

    def update(self, inventory: Inventory) -> Inventory:
        stmt = select(SqlAlchemyInventory).where(SqlAlchemyInventory.product_id == inventory.product_id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Inventory for product {inventory.product_id} not found")
        row.stock_quantity = inventory.stock_quantity
        row.low_stock_threshold = inventory.low_stock_threshold
        row.last_updated = inventory.last_updated
        self._session.flush()
        return Inventory(
            product_id=UUID(row.product_id),
            stock_quantity=row.stock_quantity,
            low_stock_threshold=row.low_stock_threshold,
            last_updated=row.last_updated,
        )

    def get_low_stock(self, threshold: Optional[int] = None) -> List[Inventory]:
        q = select(SqlAlchemyInventory)
        rows = self._session.scalars(q).all()
        result = []
        for row in rows:
            if row.stock_quantity <= (row.low_stock_threshold if threshold is None else threshold):
                result.append(Inventory(
                    product_id=UUID(row.product_id),
                    stock_quantity=row.stock_quantity,
                    low_stock_threshold=row.low_stock_threshold,
                    last_updated=row.last_updated,
                ))
        return result