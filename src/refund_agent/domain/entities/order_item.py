from dataclasses import dataclass
from uuid import UUID

from refund_agent.domain.value_objects import Money


@dataclass(frozen=True, slots=True)
class OrderItem:
    order_item_id: UUID
    product_id: str
    product_name: str
    quantity: int
    unit_price: Money
    refundable: bool = True

    def __post_init__(self) -> None:
        if not self.product_id.strip():
            raise ValueError("Product ID cannot be empty.")

        if not self.product_name.strip():
            raise ValueError("Product name cannot be empty.")

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

    @property
    def subtotal(self) -> Money:
        return Money.from_amount(
            self.unit_price.amount * self.quantity,
            self.unit_price.currency,
        )
