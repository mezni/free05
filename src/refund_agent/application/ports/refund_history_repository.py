from typing import Protocol
from uuid import UUID

from refund_agent.domain.value_objects.money import Money


class RefundHistoryRepository(Protocol):
    def get_refunded_amount(
        self,
        order_id: UUID,
        order_item_id: UUID,
    ) -> Money:
        """Return the total successfully refunded amount for an order item."""
