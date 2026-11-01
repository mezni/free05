from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from refund_agent.domain.exceptions import (
    CurrencyMismatchError,
    InsufficientFundsError,
    InvalidMoneyError,
)

_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable monetary value with currency-aware arithmetic."""

    amount: Decimal
    currency: str = "CAD"

    def __post_init__(self) -> None:
        amount = self._to_decimal(self.amount)
        currency = self.currency.strip().upper()

        if not _CURRENCY_PATTERN.fullmatch(currency):
            raise InvalidMoneyError("Currency must be a three-letter uppercase code.")

        if amount < Decimal("0"):
            raise InvalidMoneyError("Money amount cannot be negative.")

        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", currency)

    @staticmethod
    def _to_decimal(value: Decimal | int | str) -> Decimal:
        if isinstance(value, bool) or isinstance(value, float):
            raise InvalidMoneyError(
                "Money must be created using Decimal, int, or str; "
                "float values are not supported."
            )

        try:
            amount = Decimal(value)
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise InvalidMoneyError("Invalid monetary amount.") from exc

        if not amount.is_finite():
            raise InvalidMoneyError("Money amount must be finite.")

        return amount

    @classmethod
    def from_amount(
        cls,
        amount: Decimal | int | str,
        currency: str = "CAD",
    ) -> Money:
        """Create Money from a safe numeric representation."""
        return cls(amount=cls._to_decimal(amount), currency=currency)

    def _ensure_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Currency mismatch: {self.currency} != {other.currency}"
            )

    def add(self, other: Money) -> Money:
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: Money) -> Money:
        self._ensure_same_currency(other)

        if other.amount > self.amount:
            raise InsufficientFundsError(
                "Subtraction cannot produce a negative Money amount."
            )

        return Money(self.amount - other.amount, self.currency)

    def is_greater_than(self, other: Money) -> bool:
        self._ensure_same_currency(other)
        return self.amount > other.amount

    def is_greater_than_or_equal(self, other: Money) -> bool:
        self._ensure_same_currency(other)
        return self.amount >= other.amount

    def is_equal_to(self, other: Money) -> bool:
        self._ensure_same_currency(other)
        return self.amount == other.amount

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"
