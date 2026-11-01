from dataclasses import dataclass

from refund_agent.domain.enums.policy_outcome import PolicyOutcome
from refund_agent.domain.exceptions import DomainError
from refund_agent.domain.value_objects.money import Money


@dataclass(frozen=True, slots=True)
class RefundDecision:
    outcome: PolicyOutcome
    explanation: str
    policy_ids: tuple[str, ...] = ()
    calculated_amount: Money | None = None
    approval_required: bool = False
    evidence_required: bool = False

    def __post_init__(self) -> None:
        explanation = self.explanation.strip()
        if not explanation:
            raise DomainError("Decision explanation cannot be blank.")
        object.__setattr__(self, "explanation", explanation)

        normalized_policy_ids = tuple(
            policy_id.strip() for policy_id in self.policy_ids
        )
        if any(not policy_id for policy_id in normalized_policy_ids):
            raise DomainError("Policy IDs cannot be blank.")
        object.__setattr__(self, "policy_ids", normalized_policy_ids)

        if (
            self.outcome == PolicyOutcome.INELIGIBLE
            and self.calculated_amount is not None
        ):
            raise DomainError(
                "An ineligible decision cannot have a calculated refund amount."
            )

        if self.outcome == PolicyOutcome.ELIGIBLE and self.calculated_amount is None:
            raise DomainError(
                "An eligible decision must include a calculated refund amount."
            )

        if self.calculated_amount is not None and self.calculated_amount.amount <= 0:
            raise DomainError("Calculated refund amount must be greater than zero.")
