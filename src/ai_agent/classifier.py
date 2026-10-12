import re
from typing import Any

from ai_agent.models import RawTicketInput, TicketCategory, TicketClassification


def classify_ticket_payload(payload: dict[str, Any]) -> TicketClassification:
    """Classifies customer tickets safely with audit logging and fallback flags."""
    # 1. Enforce strict input contract (fails on bad types or empty text)
    input_data = RawTicketInput.model_validate(payload)
    text = input_data.text
    text_lower = text.lower()

    assumptions: list[str] = []

    # 2. Extract metadata
    order_match = re.search(r"#?(\d{4,10})\b", text)
    order_id = order_match.group(1) if order_match else None

    # 3. Keyword categorization triggers
    has_refund_kw = any(kw in text_lower for kw in ["refund", "return", "chargeback", "money back"])
    has_shipping_kw = any(kw in text_lower for kw in ["order", "arrived", "shipping", "tracking", "delivery", "where is"])

    # 4. Deterministic Precedence Logic
    if has_refund_kw:
        category = TicketCategory.REFUND_DISPUTE
        confidence = 0.95 if order_id else 0.80
        if not order_id:
            assumptions.append("Refund requested without order_id; flagged for follow-up.")
        else:
            assumptions.append("Precedence rule: Refund intent prioritized over general order query.")

    elif has_shipping_kw or order_id:
        category = TicketCategory.ORDER_STATUS
        if order_id:
            confidence = 0.98
        else:
            confidence = 0.70
            assumptions.append("Order query missing order_id; manual lookup or customer prompt required.")

    else:
        category = TicketCategory.GENERAL_INQUIRY
        confidence = 0.60
        assumptions.append("Low confidence fallback to general inquiry.")

    # 5. Operational Flags
    needs_lookup = order_id is not None
    needs_human = confidence < 0.75 or (category == TicketCategory.REFUND_DISPUTE and not order_id)

    return TicketClassification(
        category=category,
        confidence=confidence,
        order_id=order_id,
        needs_order_lookup=needs_lookup,
        needs_human_review=needs_human,
        assumptions=assumptions,
    )


def classify_ticket(text: str) -> TicketClassification:
    """Backward-compatible wrapper: classifies a raw ticket string."""
    return classify_ticket_payload({"text": text})
