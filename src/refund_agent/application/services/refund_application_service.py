from refund_agent.application.exceptions import OrderNotFoundError
from refund_agent.application.ports.order_repository import OrderRepository
from refund_agent.application.ports.refund_history_repository import (
    RefundHistoryRepository,
)
from refund_agent.application.results.refund_evaluation_result import (
    RefundEvaluationResult,
)
from refund_agent.domain.entities.refund_request import RefundRequest
from refund_agent.domain.services.refund_policy_engine import RefundPolicyEngine


class RefundApplicationService:
    """Coordinates refund evaluation without owning business policy."""

    def __init__(
        self,
        order_repository: OrderRepository,
        refund_history_repository: RefundHistoryRepository,
        policy_engine: RefundPolicyEngine,
    ) -> None:
        self._order_repository = order_repository
        self._refund_history_repository = refund_history_repository
        self._policy_engine = policy_engine

    def evaluate_refund(
        self,
        request: RefundRequest,
        *,
        evidence_verified: bool = False,
    ) -> RefundEvaluationResult:
        order = self._order_repository.get_by_id(request.order_id)

        if order is None:
            raise OrderNotFoundError(f"Order '{request.order_id}' was not found.")

        previously_refunded_amount = (
            self._refund_history_repository.get_refunded_amount(
                request.order_id,
                request.order_item_id,
            )
        )

        decision = self._policy_engine.evaluate(
            request,
            order,
            previously_refunded_amount=previously_refunded_amount,
            evidence_verified=evidence_verified,
        )

        return RefundEvaluationResult(
            refund_request_id=request.refund_request_id,
            order_id=request.order_id,
            customer_id=request.customer_id,
            decision=decision,
        )
