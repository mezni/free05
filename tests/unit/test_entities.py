from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from refund_agent.domain.entities import Customer, Order, OrderItem
from refund_agent.domain.enums import CustomerTier, OrderStatus
from refund_agent.domain.value_objects import Money


def make_item(
    *,
    quantity: int = 1,
    price: str = "25.00",
    refundable: bool = True,
) -> OrderItem:
    return OrderItem(
        order_item_id=uuid4(),
        product_id="PROD-001",
        product_name="Wireless Headphones",
        quantity=quantity,
        unit_price=Money.from_amount(price, "CAD"),
        refundable=refundable,
    )


def test_customer_normalizes_email() -> None:
    customer = Customer(
        customer_id=uuid4(),
        email="  CUSTOMER@EXAMPLE.COM ",
    )

    assert customer.email == "customer@example.com"
    assert customer.tier == CustomerTier.STANDARD
    assert customer.active


@pytest.mark.parametrize("email", ["", "   ", "invalid-email"])
def test_customer_rejects_invalid_email(email: str) -> None:
    with pytest.raises(ValueError):
        Customer(customer_id=uuid4(), email=email)


def test_order_item_calculates_subtotal() -> None:
    item = make_item(quantity=2, price="19.99")

    assert item.subtotal == Money.from_amount("39.98", "CAD")


def test_order_item_rejects_zero_quantity() -> None:
    with pytest.raises(ValueError, match="Quantity"):
        make_item(quantity=0)


def test_order_requires_at_least_one_item() -> None:
    with pytest.raises(ValueError, match="at least one item"):
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            status=OrderStatus.CONFIRMED,
            items=(),
            created_at=datetime.now(UTC),
        )


def test_delivered_order_requires_delivery_timestamp() -> None:
    with pytest.raises(ValueError, match="delivery timestamp"):
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            status=OrderStatus.DELIVERED,
            items=(make_item(),),
            created_at=datetime.now(UTC),
        )


def test_order_calculates_total_amount() -> None:
    first = make_item(quantity=2, price="25.00")
    second = make_item(quantity=1, price="10.50")

    order = Order(
        order_id=uuid4(),
        customer_id=uuid4(),
        status=OrderStatus.CONFIRMED,
        items=(first, second),
        created_at=datetime.now(UTC),
    )

    assert order.total_amount == Money.from_amount("60.50", "CAD")


def test_order_can_find_item_by_id() -> None:
    item = make_item()
    order = Order(
        order_id=uuid4(),
        customer_id=uuid4(),
        status=OrderStatus.CONFIRMED,
        items=(item,),
        created_at=datetime.now(UTC),
    )

    assert order.get_item(item.order_item_id) == item
    assert order.get_item(uuid4()) is None


def test_order_rejects_delivery_before_creation() -> None:
    created_at = datetime.now(UTC)
    delivered_at = created_at - timedelta(days=1)

    with pytest.raises(ValueError, match="precede"):
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            status=OrderStatus.DELIVERED,
            items=(make_item(),),
            created_at=created_at,
            delivered_at=delivered_at,
        )


def test_order_rejects_mixed_currencies() -> None:
    cad_item = make_item()
    usd_item = OrderItem(
        order_item_id=uuid4(),
        product_id="PROD-002",
        product_name="USB Cable",
        quantity=1,
        unit_price=Money.from_amount("5.00", "USD"),
    )

    with pytest.raises(ValueError, match="same currency"):
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            status=OrderStatus.CONFIRMED,
            items=(cad_item, usd_item),
            created_at=datetime.now(UTC),
        )
