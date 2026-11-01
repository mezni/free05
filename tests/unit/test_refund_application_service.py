from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from refund_agent.application.exceptions import OrderNotFoundError
from refund_agent.application.services.refund_application_service import (
    RefundApplicationService,
)
from refund_agent.domain.entities.order import Order
from refund_agent.domain.entities.order_item import OrderItem
from refund_agent.domain.entities.refund_request import RefundRequest
from refund_agent.domain.enums.order_status import OrderStatus
from refund_agent.domain.enums.policy_outcome import PolicyOutcome
from refund_agent.domain.enums.refund_reason import RefundReason
from refund_agent.domain.services.refund_policy_engine import RefundPolicyEngine
from refund_agent.domain.value_objects.money import Money

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


class FakeOrderRepository:
    def __init__(self, order: Order | None) -> None:
        self.order = order
        self.requested_order_id = None

    def get_by_id(self, order_id):
        self.requested_order_id = order_id
        return self.order


class FakeRefundHistoryRepository:
    def __init__(self, refunded_amount: Money) -> None:
        self.refunded_amount = refunded_amount
        self.requested_order_id = None
        self.requested_item_id = None

    def get_refunded_amount(self, order_id, order_item_id):
        self.requested_order_id = order_id
        self.requested_item_id = order_item_id
        return self.refunded_amount


def make_order_and_request():
    order_id = uuid4()
    customer_id = uuid4()

    item = OrderItem(
        order_item_id=uuid4(),
        product_id="product-123",
        product_name="Wireless Headphones",
        quantity=2,
        unit_price=Money(Decimal("50.00"), "CAD"),
    )

    order = Order(
        order_id=order_id,
        customer_id=customer_id,
        status=OrderStatus.DELIVERED,
        items=(item,),
        created_at=NOW - timedelta(days=20),
        delivered_at=NOW - timedelta(days=10),
    )

    request = RefundRequest(
        order_id=order_id,
        customer_id=customer_id,
        order_item_id=item.order_item_id,
        requested_quantity=1,
        reason=RefundReason.CUSTOMER_REMORSE,
        created_at=NOW,
    )

    return order, item, request


def make_service(
    order: Order | None,
    refunded_amount: Money | None = None,
):
    order_repository = FakeOrderRepository(order)
    history_repository = FakeRefundHistoryRepository(
        refunded_amount or Money(Decimal("0.00"), "CAD")
    )
    service = RefundApplicationService(
        order_repository=order_repository,
        refund_history_repository=history_repository,
        policy_engine=RefundPolicyEngine(),
    )
    return service, order_repository, history_repository


def test_evaluates_refund_using_order_and_history() -> None:
    order, item, request = make_order_and_request()
    service, order_repository, history_repository = make_service(order)

    result = service.evaluate_refund(request)

    assert result.refund_request_id == request.refund_request_id
    assert result.order_id == order.order_id
    assert result.customer_id == order.customer_id
    assert result.decision.outcome == PolicyOutcome.ELIGIBLE
    assert result.decision.calculated_amount == Money(
        Decimal("50.00"),
        "CAD",
    )
    assert order_repository.requested_order_id == order.order_id
    assert history_repository.requested_order_id == order.order_id
    assert history_repository.requested_item_id == item.order_item_id


def test_previous_refunds_are_passed_to_policy_engine() -> None:
    order, _, request = make_order_and_request()
    service, _, _ = make_service(
        order,
        refunded_amount=Money(Decimal("20.00"), "CAD"),
    )

    result = service.evaluate_refund(request)

    assert result.decision.calculated_amount == Money(
        Decimal("30.00"),
        "CAD",
    )


def test_missing_order_raises_application_error() -> None:
    _, _, request = make_order_and_request()
    service, _, _ = make_service(None)

    with pytest.raises(OrderNotFoundError):
        service.evaluate_refund(request)


def test_evidence_verification_is_forwarded_to_policy_engine() -> None:
    order, _, request = make_order_and_request()
    damaged_request = RefundRequest(
        order_id=request.order_id,
        customer_id=request.customer_id,
        order_item_id=request.order_item_id,
        requested_quantity=request.requested_quantity,
        reason=RefundReason.DAMAGED_ITEM,
        created_at=request.created_at,
    )
    service, _, _ = make_service(order)

    result = service.evaluate_refund(
        damaged_request,
        evidence_verified=True,
    )

    # Evidence verification does not itself approve the refund.
    assert result.decision.outcome == PolicyOutcome.NEEDS_REVIEW
    assert result.decision.evidence_required is False
