"""Shipment use cases for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4

from domain.entities import Shipment, ShipmentStatus, Carrier, Order


def create_shipment(
    *,
    order: Order,
    carrier: Carrier,
    estimated_delivery_date: Optional[datetime] = None,
) -> Shipment:
    """Create a new shipment for an order.

    FR-11: System MUST create shipments linked to orders.
    FR-12: System MUST assign a carrier: FedEx, UPS, or DHL.
    FR-13: System MUST track shipments via tracking number.
    FR-15: System MUST set estimated delivery dates.
    FR-23: System MUST return package location, carrier, and estimated delivery date.
    """
    if not order:
        raise ValueError("Order is required")
    if not carrier:
        raise ValueError("Carrier is required")

    # Generate tracking number
    tracking_number = f"TRK-{uuid4().hex[:12].upper()}"

    shipment = Shipment(
        order_id=order.id,
        carrier=carrier,
        tracking_number=tracking_number,
        status=ShipmentStatus.Label_Created,
        estimated_delivery_date=estimated_delivery_date or datetime.now() + timedelta(days=7),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    return shipment


def advance_shipment_status(
    shipment: Shipment,
    new_status: ShipmentStatus,
) -> Shipment:
    """Advance shipment status.

    FR-14: System MUST update delivery status through In Transit → Out for Delivery → Delivered.
    """
    if not shipment:
        raise ValueError("Shipment is required")

    # Validate transition
    valid_transitions = {
        ShipmentStatus.Label_Created: [ShipmentStatus.In_Transit],
        ShipmentStatus.In_Transit: [ShipmentStatus.Out_for_Delivery],
        ShipmentStatus.Out_for_Delivery: [ShipmentStatus.Delivered],
    }

    allowed_next = valid_transitions.get(shipment.status, [])
    if new_status not in allowed_next:
        raise ValueError(
            f"Invalid status transition from {shipment.status} to {new_status}. "
            f"Allowed next: {allowed_next}"
        )

    shipment.status = new_status
    shipment.updated_at = datetime.now()

    return shipment


def get_shipment_tracking_info(
    shipment: Shipment,
) -> dict:
    """Get shipment tracking information.

    FR-23: System MUST return package location, carrier, and estimated delivery date.
    """
    if not shipment:
        raise ValueError("Shipment is required")

    return {
        "tracking_number": shipment.tracking_number,
        "carrier": shipment.carrier,
        "status": shipment.status,
        "estimated_delivery_date": shipment.estimated_delivery_date.isoformat()
        if shipment.estimated_delivery_date
        else None,
        "created_at": shipment.created_at.isoformat() if shipment.created_at else None,
    }


def calculate_shipment_eta(
    shipment: Shipment,
) -> Optional[datetime]:
    """Calculate estimated delivery date for a shipment.

    FR-15: System MUST set estimated delivery dates.
    """
    if not shipment:
        return None

    # If already delivered, return now
    if shipment.status == ShipmentStatus.Delivered:
        return datetime.now()

    # Otherwise, calculate based on status and created date
    days_in_transit = (datetime.now() - shipment.created_at).days

    eta_calculations = {
        ShipmentStatus.Label_Created: 7,
        ShipmentStatus.In_Transit: 5,
        ShipmentStatus.Out_for_Delivery: 2,
        ShipmentStatus.Delivered: 0,
    }

    days_until_delivery = eta_calculations.get(shipment.status, 7)
    return datetime.now() + timedelta(days=days_until_delivery)