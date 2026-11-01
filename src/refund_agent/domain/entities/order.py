from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from refund_agent.domain.entities.order_item import OrderItem
from refund_agent.domain.enums import OrderStatus
from refund_agent.domain.value_objects import Money


@dataclass(frozen=True, slots=True)
class Order:
    order_id: UUID
    customer_id: UUID
    status: OrderStatus
    items: tuple[OrderItem, ...]
    created_at: datetime
    delivered_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("Order must contain at least one item.")

        if self.status == OrderStatus.DELIVERED and self.delivered_at is None:
            raise ValueError("Delivered order must have a delivery timestamp.")

        if self.delivered_at is not None and self.delivered_at < self.created_at:
            raise ValueError("Delivery timestamp cannot precede order creation.")

        item_ids = [item.order_item_id for item in self.items]
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("Order cannot contain duplicate item IDs.")

        currencies = {item.unit_price.currency for item in self.items}
        if len(currencies) != 1:
            raise ValueError("All order items must use the same currency.")

    @property
    def total_amount(self) -> Money:
        currency = self.items[0].unit_price.currency
        total = sum(
            (item.subtotal.amount for item in self.items),
            start=Money.from_amount("0", currency).amount,
        )
        return Money.from_amount(total, currency)

    def get_item(self, order_item_id: UUID) -> OrderItem | None:
        return next(
            (item for item in self.items if item.order_item_id == order_item_id),
            None,
        )
