"""SQLAlchemy shipment repository implementing the ShipmentRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyShipment
from domain.entities import Shipment
from domain.ports.repositories import ShipmentRepositoryPort


class SqlAlchemyShipmentRepository(ShipmentRepositoryPort):
    """SQLAlchemy implementation of ShipmentRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, shipment_id: UUID) -> Optional[Shipment]:
        stmt = select(SqlAlchemyShipment).where(SqlAlchemyShipment.id == str(shipment_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Shipment(
            id=UUID(row.id),
            order_id=UUID(row.order_id),
            tracking_number=row.tracking_number,
            carrier=row.carrier,
            status=row.status,
            estimated_delivery_date=row.estimated_delivery_date,
            created_at=row.created_at,
        )

    def get_by_order_id(self, order_id: UUID) -> Optional[Shipment]:
        stmt = select(SqlAlchemyShipment).where(SqlAlchemyShipment.order_id == str(order_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Shipment(
            id=UUID(row.id),
            order_id=UUID(row.order_id),
            tracking_number=row.tracking_number,
            carrier=row.carrier,
            status=row.status,
            estimated_delivery_date=row.estimated_delivery_date,
            created_at=row.created_at,
        )

    def get_by_tracking(self, tracking_number: str) -> Optional[Shipment]:
        stmt = select(SqlAlchemyShipment).where(SqlAlchemyShipment.tracking_number == tracking_number)
        row = self._session.scalar(stmt)
        if not row:
            return None
        return Shipment(
            id=UUID(row.id),
            order_id=UUID(row.order_id),
            tracking_number=row.tracking_number,
            carrier=row.carrier,
            status=row.status,
            estimated_delivery_date=row.estimated_delivery_date,
            created_at=row.created_at,
        )

    def create(self, shipment: Shipment) -> Shipment:
        db_shipment = SqlAlchemyShipment(
            id=shipment.id,
            order_id=str(shipment.order_id),
            tracking_number=shipment.tracking_number,
            carrier=shipment.carrier,
            status=shipment.status,
            estimated_delivery_date=shipment.estimated_delivery_date,
            created_at=shipment.created_at,
        )
        self._session.add(db_shipment)
        self._session.flush()
        return Shipment(
            id=UUID(db_shipment.id),
            order_id=UUID(db_shipment.order_id),
            tracking_number=db_shipment.tracking_number,
            carrier=db_shipment.carrier,
            status=db_shipment.status,
            estimated_delivery_date=db_shipment.estimated_delivery_date,
            created_at=db_shipment.created_at,
        )

    def update(self, shipment: Shipment) -> Shipment:
        stmt = select(SqlAlchemyShipment).where(SqlAlchemyShipment.id == shipment.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"Shipment {shipment.id} not found")
        row.status = shipment.status
        row.estimated_delivery_date = shipment.estimated_delivery_date
        self._session.flush()
        return Shipment(
            id=UUID(row.id),
            order_id=UUID(row.order_id),
            tracking_number=row.tracking_number,
            carrier=row.carrier,
            status=row.status,
            estimated_delivery_date=row.estimated_delivery_date,
            created_at=row.created_at,
        )

    def delete(self, shipment_id: UUID) -> None:
        stmt = delete(SqlAlchemyShipment).where(SqlAlchemyShipment.id == str(shipment_id))
        self._session.execute(stmt)
        self._session.flush()