from ai_agent.classifier import classify_ticket
from ai_agent.models import TicketCategory


def test_classify_order_status_with_id() -> None:
    text = "My order #4821 has not arrived."
    result = classify_ticket(text)

    assert result.category == TicketCategory.ORDER_STATUS
    assert result.order_id == "4821"
    assert result.needs_order_lookup is True


def test_classify_order_status_without_id() -> None:
    text = "Where is my shipment?"
    result = classify_ticket(text)

    assert result.category == TicketCategory.ORDER_STATUS
    assert result.order_id is None
    assert result.needs_order_lookup is False


def test_classify_general_inquiry() -> None:
    text = "What are your business opening hours?"
    result = classify_ticket(text)

    assert result.category == TicketCategory.GENERAL_INQUIRY
    assert result.order_id is None
    assert result.needs_order_lookup is False


def test_classify_order_id_without_hash_prefix() -> None:
    text = "I am checking status for order 98231."
    result = classify_ticket(text)

    assert result.category == TicketCategory.ORDER_STATUS
    assert result.order_id == "98231"
    assert result.needs_order_lookup is True
