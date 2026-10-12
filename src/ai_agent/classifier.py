import re
from ai_agent.models import TicketCategory, TicketClassification


def classify_ticket(text: str) -> TicketClassification:
    """Pure, stateless function for ticket classification."""
    order_match = re.search(r"#?(\d{4,10})\b", text)
    order_id = order_match.group(1) if order_match else None

    text_lower = text.lower()
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
