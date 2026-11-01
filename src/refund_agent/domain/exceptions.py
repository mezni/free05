class DomainError(Exception):
    """Base exception for domain-level errors."""


class InvalidMoneyError(DomainError):
    """Raised when a Money value is invalid."""


class CurrencyMismatchError(DomainError):
    """Raised when monetary values use different currencies."""


class InsufficientFundsError(DomainError):
    """Raised when subtraction would produce a negative amount."""
