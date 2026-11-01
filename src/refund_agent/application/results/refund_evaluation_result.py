from dataclasses import dataclass
from uuid import UUID

from refund_agent.domain.value_objects.refund_decision import RefundDecision


@dataclass(frozen=True, slots=True)
class RefundEvaluationResult:
    refund_request_id: UUID
    order_id: UUID
    customer_id: UUID
    decision: RefundDecision
