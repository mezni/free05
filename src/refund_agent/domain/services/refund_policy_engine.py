from decimal import Decimal

from refund_agent.domain.entities.order import Order
from refund_agent.domain.entities.refund_request import RefundRequest
from refund_agent.domain.enums.order_status import OrderStatus
from refund_agent.domain.enums.policy_outcome import PolicyOutcome
from refund_agent.domain.enums.refund_reason import RefundReason
from refund_agent.domain.exceptions import CurrencyMismatchError, DomainError
from refund_agent.domain.policies.refund_policy import RefundPolicy
from refund_agent.domain.value_objects.money import Money
from refund_agent.domain.value_objects.refund_decision import RefundDecision


class RefundPolicyEngine:
    """Deterministic policy evaluator. It never authorizes or executes payments."""

    def __init__(self, policy: RefundPolicy | None = None) -> None:
        self._policy = policy or RefundPolicy()

    def evaluate(
        self,
        request: RefundRequest,
        order: Order,
        *,
        previously_refunded_amount: Money | None = None,
        evidence_verified: bool = False,
    ) -> RefundDecision:
        """Evaluate a refund request against order data and configured policies."""

        if request.order_id != order.order_id:
            raise DomainError("Refund request order_id does not match the order.")

        if request.customer_id != order.customer_id:
            raise DomainError("Refund request customer_id does not match the order.")

        item = order.get_item(request.order_item_id)
        if item is None:
            return self._ineligible(
                "The requested item does not belong to this order.",
                "POL-002",
            )

        if not item.refundable:
            return self._ineligible(
                "The item is marked as non-refundable.",
                "POL-002",
            )

        if request.requested_quantity > item.quantity:
            return self._ineligible(
                "Requested quantity exceeds the quantity purchased.",
                "POL-002",
            )

        if order.status == OrderStatus.CANCELLED:
            return self._review(
                "Cancelled orders require evaluation under the cancellation policy.",
                policy_ids=("POL-006",),
            )

        if order.status != OrderStatus.DELIVERED or order.delivered_at is None:
            return self._ineligible(
                "The order has not been delivered.",
                "POL-001",
            )

        if request.created_at > order.delivered_at + self._policy.return_window:
            return self._ineligible(
                f"The request is outside the "
                f"{self._policy.return_window_days}-day return window.",
                "POL-001",
            )

        item_total = Money(
            item.unit_price.amount * Decimal(request.requested_quantity),
            item.unit_price.currency,
        )

        previous_refunded_amount = previously_refunded_amount or Money(
            Decimal("0.00"),
            item.unit_price.currency,
        )

        if previous_refunded_amount.currency != item_total.currency:
            raise CurrencyMismatchError(
                "Previously refunded amount currency does not match item currency."
            )

        refundable_balance_amount = item_total.amount - previous_refunded_amount.amount

        if refundable_balance_amount <= 0:
            return self._ineligible(
                "No refundable balance remains for this request.",
                "POL-003",
            )

        refundable_balance = Money(
            refundable_balance_amount,
            item_total.currency,
        )

        policy_ids = ["POL-001", "POL-002", "POL-003"]
        approval_required = (
            refundable_balance.amount > self._policy.supervisor_approval_threshold
        )

        if approval_required:
            policy_ids.append("POL-005")

        if request.reason == RefundReason.DAMAGED_ITEM:
            policy_ids.append("POL-004")

            if not evidence_verified:
                return self._review(
                    "Damaged-item evidence must be verified by a reviewer.",
                    policy_ids=tuple(policy_ids),
                    calculated_amount=refundable_balance,
                    approval_required=approval_required,
                    evidence_required=True,
                )

            return self._review(
                "Evidence is verified; damaged-item review is still required.",
                policy_ids=tuple(policy_ids),
                calculated_amount=refundable_balance,
                approval_required=approval_required,
                evidence_required=False,
            )

        return RefundDecision(
            outcome=PolicyOutcome.ELIGIBLE,
            explanation="The request satisfies the configured refund policies.",
            policy_ids=tuple(policy_ids),
            calculated_amount=refundable_balance,
            approval_required=approval_required,
        )

    @staticmethod
    def _ineligible(explanation: str, policy_id: str) -> RefundDecision:
        return RefundDecision(
            outcome=PolicyOutcome.INELIGIBLE,
            explanation=explanation,
            policy_ids=(policy_id,),
        )

    @staticmethod
    def _review(
        explanation: str,
        *,
        policy_ids: tuple[str, ...],
        calculated_amount: Money | None = None,
        approval_required: bool = False,
        evidence_required: bool = False,
    ) -> RefundDecision:
        return RefundDecision(
            outcome=PolicyOutcome.NEEDS_REVIEW,
            explanation=explanation,
            policy_ids=policy_ids,
            calculated_amount=calculated_amount,
            approval_required=approval_required,
            evidence_required=evidence_required,
        )
