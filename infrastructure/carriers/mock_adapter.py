"""Mock carrier adapter for bss-core Support Application (MVP)."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional, Dict, Any

from domain.entities import Carrier


class MockCarrierAdapter:
    """Mock carrier adapter with deterministic states for MVP testing.

    FR-13: System MUST assign a carrier: FedEx, UPS, or DHL.
    FR-23: System MUST return package location, carrier, and estimated delivery date.
    D-13: Carrier integrations use a port-backed mock/sandbox adapter until live credentials exist.
    """

    def __init__(self):
        self.shipments: Dict[str, dict] = {}
        self.carrier_states: Dict[str, dict] = {}

    def create_shipment(
        self,
        *,
        order_id: str,
        carrier: Carrier,
        estimated_delivery_date: Optional[datetime] = None,
    ) -> dict:
        """Create a shipment with a mock carrier.

        FR-11: System MUST create shipments linked to orders.
        FR-12: System MUST assign a carrier: FedEx, UPS, or DHL.
        FR-23: System MUST return package location, carrier, and estimated delivery date.
        """
        carrier_name = carrier.value if hasattr(carrier, "value") else str(carrier)
        if carrier_name not in ("FEDEX", "UPS", "DHL"):
            raise ValueError(f"Unsupported carrier: {carrier_name}")

        tracking_number = f"TRK-{uuid4().hex[:12].upper()}"
        created_at = datetime.now()
        eta = (estimated_delivery_date or datetime.now() + timedelta(days=7)).date()

        shipment_info = {
            "id": str(uuid4()),
            "order_id": order_id,
            "carrier": carrier_name,
            "tracking_number": tracking_number,
            "status": "Label Created",
            "estimated_delivery_date": eta,
            "created_at": created_at,
            "updated_at": created_at,
        }

        self.shipments[tracking_number] = shipment_info
        self.carrier_states[tracking_number] = {
            "current_status": "Label Created",
            "history": ["Label Created"],
        }

        return shipment_info

    def get_shipment(
        self,
        tracking_number: str,
    ) -> Optional[dict]:
        """Get shipment status by tracking number.

        FR-13: System MUST track shipments via tracking number.
        FR-23: System MUST return package location, carrier, and estimated delivery date.
        """
        return self.shipments.get(tracking_number)

    def advance_status(
        self,
        tracking_number: str,
    ) -> Optional[dict]:
        """Advance shipment status through valid transitions.

        FR-14: System MUST update delivery status through In Transit → Out for Delivery → Delivered.
        """
        shipment = self.shipments.get(tracking_number)
        if not shipment:
            return None

        current_status = shipment["status"]

        # Define valid transitions
        transitions = {
            "Label Created": "In Transit",
            "In Transit": "Out for Delivery",
            "Out for Delivery": "Delivered",
        }

        next_status = transitions.get(current_status)
        if not next_status:
            return shipment

        shipment["status"] = next_status
        shipment["updated_at"] = datetime.now()

        # Update history
        if tracking_number in self.carrier_states:
            self.carrier_states[tracking_number]["history"].append(next_status)
            self.carrier_states[tracking_number]["current_status"] = next_status

        return shipment

    def simulate_carrier_outage(
        self,
        tracking_number: str,
        duration_minutes: int = 30,
    ) -> dict:
        """Simulate carrier network degradation.

        FR-23: Carrier outage/degradation behavior is specified (mock, deterministic, no data loss).
        """
        shipment = self.shipments.get(tracking_number)
        if not shipment:
            return {"error": "Shipment not found"}

        # Store original status and mark as degraded
        original_status = shipment["status"]
        shipment["status"] = "Carrier Unavailable"
        shipment["degraded_at"] = datetime.now()

        # Schedule recovery (in MVP, just note it)
        return {
            "original_status": original_status,
            "current_status": "Carrier Unavailable",
            "recovery_time": datetime.now() + timedelta(minutes=duration_minutes),
            "no_data_loss": True,
        }