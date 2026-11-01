from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class RefundPolicy:
    return_window_days: int = 30
    supervisor_approval_threshold: Decimal = Decimal("100.00")
    currency: str = "CAD"

    def __post_init__(self) -> None:
        if self.return_window_days <= 0:
            raise ValueError("Return window must be greater than zero.")

        if self.supervisor_approval_threshold < Decimal("0"):
            raise ValueError("Approval threshold cannot be negative.")

        if len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError("Currency must be a three-letter code.")

    @property
    def return_window(self) -> timedelta:
        return timedelta(days=self.return_window_days)
