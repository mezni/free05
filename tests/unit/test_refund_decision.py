from decimal import Decimal

import pytest

from refund_agent.domain.enums.policy_outcome import PolicyOutcome
from refund_agent.domain.exceptions import DomainError
from refund_agent.domain.value_objects.money import Money
from refund_agent.domain.value_objects.refund_decision import RefundDecision


def test_eligible_decision_requires_amount() -> None:
    with pytest.raises(DomainError, match="must include"):
        RefundDecision(
            outcome=PolicyOutcome.ELIGIBLE,
            explanation="The item is within the return window.",
        )


def test_eligible_decision_with_amount() -> None:
    decision = RefundDecision(
        outcome=PolicyOutcome.ELIGIBLE,
        explanation="Eligible under the standard return policy.",
        policy_ids=("POL-001",),
        calculated_amount=Money(Decimal("49.99"), "CAD"),
    )

    assert decision.outcome == PolicyOutcome.ELIGIBLE
    assert decision.calculated_amount == Money(Decimal("49.99"), "CAD")
    assert decision.policy_ids == ("POL-001",)


def test_ineligible_decision_cannot_have_amount() -> None:
    with pytest.raises(DomainError, match="cannot have"):
        RefundDecision(
            outcome=PolicyOutcome.INELIGIBLE,
            explanation="The item is outside the return window.",
            calculated_amount=Money(Decimal("20.00"), "CAD"),
        )


def test_review_decision_can_include_estimated_amount() -> None:
    decision = RefundDecision(
        outcome=PolicyOutcome.NEEDS_REVIEW,
        explanation="Damaged item requires evidence review.",
        calculated_amount=Money(Decimal("75.00"), "CAD"),
        evidence_required=True,
    )

    assert decision.outcome == PolicyOutcome.NEEDS_REVIEW
    assert decision.evidence_required is True


def test_rejects_blank_explanation() -> None:
    with pytest.raises(DomainError, match="cannot be blank"):
        RefundDecision(
            outcome=PolicyOutcome.INELIGIBLE,
            explanation=" ",
        )


def test_rejects_non_positive_calculated_amount() -> None:
    with pytest.raises(DomainError, match="greater than zero"):
        RefundDecision(
            outcome=PolicyOutcome.ELIGIBLE,
            explanation="Eligible.",
            calculated_amount=Money(Decimal("0.00"), "CAD"),
        )


def test_rejects_blank_policy_id() -> None:
    with pytest.raises(DomainError, match="cannot be blank"):
        RefundDecision(
            outcome=PolicyOutcome.INELIGIBLE,
            explanation="Not eligible.",
            policy_ids=("POL-001", " "),
        )
