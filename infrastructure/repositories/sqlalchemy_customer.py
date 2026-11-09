"""SQLAlchemy customer repository implementing the CustomerRepositoryPort."""

from __future__ import annotations

import json
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyCustomer
from domain.entities import Customer, Tier
from domain.ports.repositories import CustomerRepositoryPort


class SqlAlchemyCustomerRepository(CustomerRepositoryPort):
    """SQLAlchemy implementation of CustomerRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        stmt = select(SqlAlchemyCustomer).where(SqlAlchemyCustomer.id == str(customer_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Customer(
            id=UUID(row.id),
            name=row.name,
            email=row.email,
            tier=Tier(row.tier) if row.tier else Tier.Standard,
            preferences=json.loads(row.preferences) if row.preferences else {},
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def get_by_email(self, email: str) -> Optional[Customer]:
        stmt = select(SqlAlchemyCustomer).where(SqlAlchemyCustomer.email == email)
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Customer(
            id=UUID(row.id),
            name=row.name,
            email=row.email,
            tier=Tier(row.tier) if row.tier else Tier.Standard,
            preferences=json.loads(row.preferences) if row.preferences else {},
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def create(self, customer: Customer) -> Customer:
        import json
        from domain.entities import Tier
        prefs = json.dumps(customer.preferences) if customer.preferences else None
        db_customer = SqlAlchemyCustomer(
            id=str(customer.id),
            name=customer.name,
            email=customer.email,
            tier=customer.tier.value if isinstance(customer.tier, Tier) else customer.tier,
            preferences=prefs,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
        )
        self._session.add(db_customer)
        self._session.flush()
        return Customer(
            id=UUID(db_customer.id),
            name=db_customer.name,
            email=db_customer.email,
            tier=Tier(db_customer.tier) if db_customer.tier else Tier.Standard,
            preferences=json.loads(db_customer.preferences) if db_customer.preferences else {},
            created_at=db_customer.created_at,
            updated_at=db_customer.updated_at,
        )

    def update(self, customer: Customer) -> Customer:
        import json
        from domain.entities import Tier
        # Always convert preferences to JSON string for DB storage
        prefs = json.dumps(customer.preferences) if customer.preferences else None
        stmt = select(SqlAlchemyCustomer).where(SqlAlchemyCustomer.id == str(customer.id))
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Customer {customer.id} not found")
        row.name = customer.name
        row.tier = customer.tier.value if isinstance(customer.tier, Tier) else customer.tier
        row.preferences = prefs
        row.updated_at = customer.updated_at
        self._session.flush()
        return Customer(
            id=UUID(row.id),
            name=row.name,
            email=row.email,
            tier=Tier(row.tier) if row.tier else Tier.Standard,
            preferences=json.loads(row.preferences) if isinstance(row.preferences, str) and row.preferences else (row.preferences or {}),
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def delete(self, customer_id: UUID) -> None:
        stmt = select(SqlAlchemyCustomer).where(SqlAlchemyCustomer.id == str(customer_id))
        row = self._session.scalar(stmt)
        if row:
            self._session.delete(row)
            self._session.flush()