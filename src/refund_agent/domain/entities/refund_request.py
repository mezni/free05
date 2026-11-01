from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from refund_agent.domain.enums.refund_reason import RefundReason
from refund_agent.domain.enums.refund_status import RefundStatus
from refund_agent.domain.exceptions import DomainError


@dataclass(frozen=True, slots=True)
class RefundRequest:
    order_id: UUID
    customer_id: UUID
    order_item_id: UUID
    requested_quantity: int
    reason: RefundReason
    customer_note: str | None = None
    refund_request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    status: RefundStatus = RefundStatus.RECEIVED

    def __post_init__(self) -> None:
        if self.requested_quantity <= 0:
            raise DomainError("Requested quantity must be greater than zero.")

        if self.customer_note is not None:
            note = self.customer_note.strip()
            if not note:
                raise DomainError("Customer note cannot be blank.")
            if len(note) > 2000:
                raise DomainError("Customer note cannot exceed 2000 characters.")
            object.__setattr__(self, "customer_note", note)

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise DomainError("Refund request created_at must be timezone-aware.")
