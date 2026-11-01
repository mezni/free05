from dataclasses import dataclass
from uuid import UUID

from refund_agent.domain.enums import CustomerTier


@dataclass(frozen=True, slots=True)
class Customer:
    customer_id: UUID
    email: str
    tier: CustomerTier = CustomerTier.STANDARD
    active: bool = True

    def __post_init__(self) -> None:
        normalized_email = self.email.strip().lower()

        if not normalized_email:
            raise ValueError("Customer email cannot be empty.")

        if "@" not in normalized_email:
            raise ValueError("Customer email must be valid.")

        object.__setattr__(self, "email", normalized_email)
