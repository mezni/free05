"""SQLAlchemy product repository implementing the ProductRepositoryPort."""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyProduct
from domain.entities import Product
from domain.ports.repositories import ProductRepositoryPort


class SqlAlchemyProductRepository(ProductRepositoryPort):
    """SQLAlchemy implementation of ProductRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        stmt = select(SqlAlchemyProduct).where(SqlAlchemyProduct.id == str(product_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Product(
            id=UUID(row.id),
            sku=row.sku,
            name=row.name,
            description=row.description,
            unit_price=Decimal(row.unit_price),
            category=row.category,
            active=row.active,
        )

    def get_by_sku(self, sku: str) -> Optional[Product]:
        stmt = select(SqlAlchemyProduct).where(SqlAlchemyProduct.sku == sku)
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Product(
            id=UUID(row.id),
            sku=row.sku,
            name=row.name,
            description=row.description,
            unit_price=Decimal(row.unit_price),
            category=row.category,
            active=row.active,
        )

    def get_active(self) -> List[Product]:
        stmt = select(SqlAlchemyProduct).where(SqlAlchemyProduct.active == True)
        rows = self._session.scalars(stmt).all()
        return [
            Product(
                id=UUID(row.id),
                sku=row.sku,
                name=row.name,
                description=row.description,
                unit_price=Decimal(row.unit_price),
                category=row.category,
                active=row.active,
            )
            for row in rows
        ]

    def create(self, product: Product) -> Product:
        db_product = SqlAlchemyProduct(
            id=str(product.id),
            sku=product.sku,
            name=product.name,
            description=product.description,
            unit_price=product.unit_price,
            category=product.category,
            active=product.active,
        )
        self._session.add(db_product)
        self._session.flush()
        return Product(
            id=UUID(db_product.id),
            sku=db_product.sku,
            name=db_product.name,
            description=db_product.description,
            unit_price=db_product.unit_price,
            category=db_product.category,
            active=db_product.active,
        )

    def update(self, product: Product) -> Product:
        stmt = select(SqlAlchemyProduct).where(SqlAlchemyProduct.id == product.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Product {product.id} not found")
        row.sku = product.sku
        row.name = product.name
        row.description = product.description
        row.unit_price = product.unit_price
        row.category = product.category
        row.active = product.active
        self._session.flush()
        return Product(
            id=UUID(row.id),
            sku=row.sku,
            name=row.name,
            description=row.description,
            unit_price=Decimal(row.unit_price),
            category=row.category,
            active=row.active,
        )

    def delete(self, product_id: UUID) -> None:
        stmt = select(SqlAlchemyProduct).where(SqlAlchemyProduct.id == str(product_id))
        row = self._session.scalar(stmt)
        if row:
            self._session.delete(row)
            self._session.flush()