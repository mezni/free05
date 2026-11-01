from datetime import UTC, datetime
from uuid import uuid4

import pytest

from refund_agent.domain.entities.refund_request import RefundRequest
from refund_agent.domain.enums.refund_reason import RefundReason
from refund_agent.domain.enums.refund_status import RefundStatus
from refund_agent.domain.exceptions import DomainError


def make_request(**overrides) -> RefundRequest:
    values = {
        "order_id": uuid4(),
        "customer_id": uuid4(),
        "order_item_id": uuid4(),
        "requested_quantity": 1,
        "reason": RefundReason.DAMAGED_ITEM,
    }
    values.update(overrides)
    return RefundRequest(**values)


def test_creates_refund_request_with_defaults() -> None:
    request = make_request()

    assert request.refund_request_id is not None
    assert request.status == RefundStatus.RECEIVED
    assert request.created_at.tzinfo is not None


def test_rejects_zero_quantity() -> None:
    with pytest.raises(DomainError, match="greater than zero"):
        make_request(requested_quantity=0)


def test_rejects_negative_quantity() -> None:
    with pytest.raises(DomainError, match="greater than zero"):
        make_request(requested_quantity=-1)


def test_normalizes_customer_note() -> None:
    request = make_request(customer_note="  Item arrived damaged.  ")

    assert request.customer_note == "Item arrived damaged."


def test_rejects_blank_customer_note() -> None:
    with pytest.raises(DomainError, match="cannot be blank"):
        make_request(customer_note="   ")


def test_rejects_note_over_2000_characters() -> None:
    with pytest.raises(DomainError, match="2000"):
        make_request(customer_note="x" * 2001)


def test_rejects_naive_datetime() -> None:
    with pytest.raises(DomainError, match="timezone-aware"):
        make_request(created_at=datetime(2026, 1, 1))


def test_accepts_timezone_aware_datetime() -> None:
    created_at = datetime(2026, 1, 1, tzinfo=UTC)

    request = make_request(created_at=created_at)

    assert request.created_at == created_at
