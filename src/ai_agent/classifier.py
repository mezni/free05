import re
from typing import Any

from ai_agent.models import RawTicketInput, TicketCategory, TicketClassification


def classify_ticket_payload(payload: dict[str, Any]) -> TicketClassification:
    """Validate dict payload against RawTicketInput contract."""

    # 1. Enforce strict input contract (ignores unknown keys, validates fields)
    ticket_data = RawTicketInput.model_validate(payload)

    # 2. Extract metadata safely from validated text
    order_match = re.search(r"#?(\d{4,10})\b", ticket_data.text)
    order_id = order_match.group(1) if order_match else None

    text_lower = ticket_data.text.lower()
    is_order_query = any(
        kw in text_lower
        for kw in ["order", "arrived", "shipping", "shipment", "tracking", "delivered"]
    )

    if is_order_query or order_id:
        category = TicketCategory.ORDER_STATUS
        needs_lookup = order_id is not None
    else:
        category = TicketCategory.GENERAL_INQUIRY
        needs_lookup = False

    return TicketClassification(
        category=category,
        order_id=order_id,
        needs_order_lookup=needs_lookup,
    )


def classify_ticket(text: str) -> TicketClassification:
    """Backward-compatible wrapper: classifies a raw ticket string."""
    return classify_ticket_payload({"text": text})
