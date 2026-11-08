"""Shipment routes for bss-core Support Application API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Status
from typing import List, Optional

from application.use_cases.shipments import (
    create_shipment,
    advance_shipment_status,
    get_shipment_tracking_info,
    calculate_shipment_eta,
)
from infrastructure.carriers.mock_adapter import MockCarrierAdapter
from api.deps import get_current_user_with_scope
from domain.entities import Order, ShipmentStatus, Carrier

router = APIRouter(prefix="/shipments", tags=["shipments"])


carrier_adapter = MockCarrierAdapter()


@router.post(
    "",
    status_code=201,
    responses={400: {"description": "Validation error"}, 404: {"description": "Order not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def create_shipment_route(
    *,
    order_id: str,
    carrier: Carrier,
    estimated_delivery_date: Optional[str] = None,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Create a shipment for an order.

    FR-11: System MUST create shipments linked to orders.
    FR-12: System MUST assign a carrier: FedEx, UPS, or DHL.
    FR-15: System MUST set estimated delivery dates.
    FR-23: System MUST return package location, carrier, and estimated delivery date.
    """
    # Placeholder - actual order lookup via repository
    from domain.entities import Order
    order = Order(id=order_id)  # Simplified

    try:
        eta = None
        if estimated_delivery_date:
            from datetime import datetime
            eta = datetime.fromisoformat(estimated_delivery_date)

        shipment = create_shipment(
            order=order,
            carrier=carrier,
            estimated_delivery_date=eta,
        )

        # Also create in mock adapter
        adapter_shipment = carrier_adapter.create_shipment(
            order_id=order.id,
            carrier=carrier,
            estimated_delivery_date=eta,
        )

        return {
            "id": str(shipment.id),
            "order_id": shipment.order_id,
            "carrier": shipment.carrier,
            "tracking_number": shipment.tracking_number,
            "status": shipment.status,
            "estimated_delivery_date": shipment.estimated_delivery_date.isoformat()
            if shipment.estimated_delivery_date
            else None,
            "created_at": shipment.created_at.isoformat() if shipment.created_at else None,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{tracking_number}",
    responses={404: {"description": "Shipment not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_shipment_route(
    *,
    tracking_number: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get shipment by tracking number.

    FR-13: System MUST track shipments via tracking number.
    FR-23: System MUST return package location, carrier, and estimated delivery date.
    """
    shipment = carrier_adapter.get_shipment(tracking_number)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return {
        "tracking_number": shipment["tracking_number"],
        "carrier": shipment["carrier"],
        "status": shipment["status"],
        "estimated_delivery_date": shipment.get("estimated_delivery_date"),
        "created_at": shipment.get("created_at"),
    }


@router.post(
    "/{tracking_number}/status",
    responses={
        400: {"description": "Invalid transition"},
        404: {"description": "Shipment not found"},
        401: {"description": "Unauthenticated"},
        403: {"description": "Insufficient scope"},
    },
)
async def advance_shipment_status_route(
    *,
    tracking_number: str,
    new_status: ShipmentStatus,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Advance shipment status.

    FR-14: System MUST update delivery status through In Transit → Out for Delivery → Delivered.
    """
    shipment = carrier_adapter.get_shipment(tracking_number)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    try:
        advanced = advance_shipment_status_route_inner(
            shipment=shipment,
            new_status=new_status,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "tracking_number": shipment["tracking_number"],
        "status": advanced["status"],
        "updated_at": advanced["updated_at"].isoformat() if advanced.get("updated_at") else None,
    }


def advance_shipment_status_route_inner(
    shipment: dict,
    new_status: ShipmentStatus,
) -> dict:
    """Internal function to advance shipment status."""
    advanced = carrier_adapter.advance_status(tracking_number=shipment["tracking_number"])
    return advanced


@router.get(
    "/{tracking_number}/eta",
    responses={404: {"description": "Shipment not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_shipment_eta_route(
    *,
    tracking_number: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get estimated delivery date for shipment.

    FR-15: System MUST set estimated delivery dates.
    """
    shipment = carrier_adapter.get_shipment(tracking_number)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    eta = calculate_shipment_eta_from_dict(shipment)
    return {
        "tracking_number": tracking_number,
        "estimated_delivery_date": eta.isoformat() if eta else None,
    }


def calculate_shipment_eta_from_dict(
    shipment: dict,
) -> Optional[datetime]:
    """Calculate ETA from shipment dict."""
    if not shipment:
        return None

    if shipment.get("status") == ShipmentStatus.Delivered.value:
        return datetime.now()

    days_map = {
        "Label Created": 7,
        "In Transit": 5,
        "Out for Delivery": 2,
        "Delivered": 0,
    }

    days_until = days_map.get(shipment.get("status", ""), 7)
    return datetime.now() + timedelta(days=days_until)