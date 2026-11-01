from typing import Protocol
from uuid import UUID

from refund_agent.domain.entities.order import Order


class OrderRepository(Protocol):
    def get_by_id(self, order_id: UUID) -> Order | None:
        """Return an order by ID, or None if it does not exist."""
