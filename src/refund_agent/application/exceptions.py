class ApplicationError(Exception):
    """Base exception for application-layer failures."""


class OrderNotFoundError(ApplicationError):
    """Raised when the requested order cannot be found."""


class RefundHistoryUnavailableError(ApplicationError):
    """Raised when refund history cannot be retrieved."""
