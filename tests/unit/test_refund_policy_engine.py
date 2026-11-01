from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from refund_agent.domain.entities.order import Order
from refund_agent.domain.entities.order_item import OrderItem
from refund_agent.domain.entities.refund_request import RefundRequest
from refund_agent.domain.enums.order_status import OrderStatus
from refund_agent.domain.enums.policy_outcome import PolicyOutcome
from refund_agent.domain.enums.refund_reason import RefundReason
from refund_agent.domain.exceptions import CurrencyMismatchError, DomainError
from refund_agent.domain.services.refund_policy_engine import RefundPolicyEngine
from refund_agent.domain.value_objects.money import Money

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


def make_order(
    *,
    status: OrderStatus = OrderStatus.DELIVERED,
    delivered_at: datetime | None = NOW - timedelta(days=10),
    quantity: int = 2,
    unit_price: Decimal = Decimal("50.00"),
    refundable: bool = True,
) -> tuple[Order, OrderItem]:
    order_id = uuid4()
    customer_id = uuid4()

    item = OrderItem(
        order_item_id=uuid4(),
        product_id="product-123",
        product_name="Wireless Headphones",
        quantity=quantity,
        unit_price=Money(unit_price, "CAD"),
        refundable=refundable,
    )

    order = Order(
        order_id=order_id,
        customer_id=customer_id,
        status=status,
        items=(item,),
        created_at=NOW - timedelta(days=60),
        delivered_at=delivered_at,
    )
    return order, item


def make_request(
    order: Order,
    item: OrderItem,
    *,
    quantity: int = 1,
    reason: RefundReason = RefundReason.CUSTOMER_REMORSE,
    created_at: datetime = NOW,
) -> RefundRequest:
    return RefundRequest(
        order_id=order.order_id,
        customer_id=order.customer_id,
        order_item_id=item.order_item_id,
        requested_quantity=quantity,
        reason=reason,
        created_at=created_at,
    )


def test_eligible_request_within_return_window() -> None:
    order, item = make_order()
    request = make_request(order, item)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.ELIGIBLE
    assert decision.calculated_amount == Money(Decimal("50.00"), "CAD")
    assert decision.approval_required is False


def test_request_on_last_day_of_return_window_is_eligible() -> None:
    delivered_at = NOW - timedelta(days=30)
    order, item = make_order(delivered_at=delivered_at)
    request = make_request(order, item, created_at=NOW)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.ELIGIBLE


def test_request_after_return_window_is_ineligible() -> None:
    delivered_at = NOW - timedelta(days=31)
    order, item = make_order(delivered_at=delivered_at)
    request = make_request(order, item)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.INELIGIBLE
    assert "return window" in decision.explanation


def test_non_refundable_item_is_ineligible() -> None:
    order, item = make_order(refundable=False)
    request = make_request(order, item)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.INELIGIBLE


def test_requested_quantity_cannot_exceed_purchased_quantity() -> None:
    order, item = make_order(quantity=1)
    request = make_request(order, item, quantity=2)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.INELIGIBLE


def test_non_delivered_order_is_ineligible() -> None:
    order, item = make_order(
        status=OrderStatus.SHIPPED,
        delivered_at=None,
    )
    request = make_request(order, item)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.INELIGIBLE


def test_cancelled_order_requires_review() -> None:
    order, item = make_order(
        status=OrderStatus.CANCELLED,
        delivered_at=None,
    )
    request = make_request(order, item)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.outcome == PolicyOutcome.NEEDS_REVIEW
    assert "POL-006" in decision.policy_ids


def test_previous_refund_reduces_refundable_balance() -> None:
    order, item = make_order(quantity=2, unit_price=Decimal("50.00"))
    request = make_request(order, item, quantity=2)

    decision = RefundPolicyEngine().evaluate(
        request,
        order,
        previously_refunded_amount=Money(Decimal("25.00"), "CAD"),
    )

    assert decision.outcome == PolicyOutcome.ELIGIBLE
    assert decision.calculated_amount == Money(Decimal("75.00"), "CAD")


def test_fully_refunded_balance_is_ineligible() -> None:
    order, item = make_order(quantity=1, unit_price=Decimal("50.00"))
    request = make_request(order, item)

    decision = RefundPolicyEngine().evaluate(
        request,
        order,
        previously_refunded_amount=Money(Decimal("50.00"), "CAD"),
    )

    assert decision.outcome == PolicyOutcome.INELIGIBLE


def test_previous_refund_currency_must_match() -> None:
    order, item = make_order()
    request = make_request(order, item)

    with pytest.raises(CurrencyMismatchError):
        RefundPolicyEngine().evaluate(
            request,
            order,
            previously_refunded_amount=Money(Decimal("10.00"), "USD"),
        )


def test_refund_of_exactly_100_does_not_require_supervisor() -> None:
    order, item = make_order(quantity=2, unit_price=Decimal("50.00"))
    request = make_request(order, item, quantity=2)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.calculated_amount == Money(Decimal("100.00"), "CAD")
    assert decision.approval_required is False


def test_refund_over_100_requires_supervisor() -> None:
    order, item = make_order(quantity=2, unit_price=Decimal("50.01"))
    request = make_request(order, item, quantity=2)

    decision = RefundPolicyEngine().evaluate(request, order)

    assert decision.calculated_amount == Money(Decimal("100.02"), "CAD")
    assert decision.approval_required is True
    assert "POL-005" in decision.policy_ids


def test_damaged_item_without_verified_evidence_requires_review() -> None:
    order, item = make_order()
    request = make_request(order, item, reason=RefundReason.DAMAGED_ITEM)

    decision = RefundPolicyEngine().evaluate(
        request,
        order,
        evidence_verified=False,
    )

    assert decision.outcome == PolicyOutcome.NEEDS_REVIEW
    assert decision.evidence_required is True
    assert decision.calculated_amount == Money(Decimal("50.00"), "CAD")


def test_damaged_item_with_verified_evidence_still_requires_review() -> None:
    order, item = make_order()
    request = make_request(order, item, reason=RefundReason.DAMAGED_ITEM)

    decision = RefundPolicyEngine().evaluate(
        request,
        order,
        evidence_verified=True,
    )

    assert decision.outcome == PolicyOutcome.NEEDS_REVIEW
    assert decision.evidence_required is False
    assert "POL-004" in decision.policy_ids


def test_request_order_id_must_match_order() -> None:
    order, item = make_order()
    request = make_request(order, item)

    different_order, _ = make_order()

    with pytest.raises(DomainError, match="order_id"):
        RefundPolicyEngine().evaluate(request, different_order)
