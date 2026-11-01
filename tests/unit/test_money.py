from decimal import Decimal

import pytest

from refund_agent.domain.exceptions import (
    CurrencyMismatchError,
    InsufficientFundsError,
    InvalidMoneyError,
)
from refund_agent.domain.value_objects import Money


def test_create_money_from_string() -> None:
    money = Money.from_amount("100.25", "CAD")

    assert money.amount == Decimal("100.25")
    assert money.currency == "CAD"


def test_currency_is_normalized_to_uppercase() -> None:
    money = Money.from_amount("12.50", "cad")

    assert money.currency == "CAD"


def test_money_is_immutable() -> None:
    money = Money.from_amount("10.00")

    with pytest.raises(AttributeError):
        money.amount = Decimal("20.00")  # type: ignore[misc]


@pytest.mark.parametrize("amount", ["-1", -1, Decimal("-0.01")])
def test_negative_amount_is_rejected(amount: str | int | Decimal) -> None:
    with pytest.raises(InvalidMoneyError):
        Money.from_amount(amount)


@pytest.mark.parametrize("amount", [10.5, True, float("nan"), float("inf")])
def test_unsafe_or_non_finite_amount_is_rejected(amount: float | bool) -> None:
    with pytest.raises(InvalidMoneyError):
        Money.from_amount(amount)  # type: ignore[arg-type]


@pytest.mark.parametrize("currency", ["", "CA", "CAD1", "123", "ca!"])
def test_invalid_currency_is_rejected(currency: str) -> None:
    with pytest.raises(InvalidMoneyError):
        Money.from_amount("10.00", currency)


def test_add_money_with_same_currency() -> None:
    first = Money.from_amount("10.25", "CAD")
    second = Money.from_amount("2.75", "CAD")

    result = first.add(second)

    assert result == Money.from_amount("13.00", "CAD")


def test_subtract_money_with_same_currency() -> None:
    first = Money.from_amount("10.00", "CAD")
    second = Money.from_amount("3.25", "CAD")

    result = first.subtract(second)

    assert result == Money.from_amount("6.75", "CAD")


def test_subtraction_cannot_produce_negative_amount() -> None:
    first = Money.from_amount("5.00", "CAD")
    second = Money.from_amount("6.00", "CAD")

    with pytest.raises(InsufficientFundsError):
        first.subtract(second)


def test_addition_rejects_currency_mismatch() -> None:
    cad = Money.from_amount("10.00", "CAD")
    usd = Money.from_amount("5.00", "USD")

    with pytest.raises(CurrencyMismatchError):
        cad.add(usd)


def test_comparison_rejects_currency_mismatch() -> None:
    cad = Money.from_amount("10.00", "CAD")
    usd = Money.from_amount("10.00", "USD")

    with pytest.raises(CurrencyMismatchError):
        cad.is_greater_than(usd)


def test_greater_than_comparison() -> None:
    first = Money.from_amount("100.01")
    second = Money.from_amount("100.00")

    assert first.is_greater_than(second)
    assert not second.is_greater_than(first)


def test_money_string_format() -> None:
    money = Money.from_amount("100")

    assert str(money) == "CAD 100.00"
