"""Тесты для калькулятора: tokenize, validate, resolve_unary, calculate."""

import pytest

from toolkit.calculator import calculate, resolve_unary, tokenize, validate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingNumError,
    MissingOperatorError,
    TwoBinaryOperatorsError,
)


def run(expr: str) -> float:
    """Прогоняет выражение через полный пайплайн калькулятора."""
    tokens = tokenize(expr)
    validate(tokens)
    return calculate(tokens)


# --- Позитивные тесты ---

def test_simple_addition():
    """Проверяет базовое сложение."""
    assert run("2 + 2") == 4.0


def test_operator_priority():
    """Проверяет, что умножение выполняется раньше сложения."""
    assert run("2 + 3 * 4") == 14.0


def test_division():
    """Проверяет деление вещественных чисел."""
    assert run("10 / 4") == 2.5


def test_unary_minus_at_start():
    """Проверяет унарный минус в начале выражения."""
    assert run("-5 + 10") == 5.0


def test_unary_plus_after_operator():
    """Проверяет унарный плюс после бинарного оператора."""
    assert run("5 * +3") == 15.0


def test_unary_minus_after_operator():
    """Проверяет унарный минус после бинарного оператора."""
    assert run("5 * -3") == -15.0


def test_ignores_whitespace():
    """Проверяет, что пробелы между токенами игнорируются."""
    assert run("2+2") == run("2 + 2")


def test_float_numbers():
    """Проверяет работу с вещественными числами."""
    assert run("1.5 + 2.5") == 4.0


def test_chained_multiplication():
    """Проверяет цепочку из нескольких операций умножения."""
    assert run("2 * 3 * 4") == 24.0


def test_mixed_priority_expression():
    """Проверяет смешанное выражение с разными приоритетами."""
    assert run("10 - 2 * 3 + 4 / 2") == 6.0


def test_resolve_unary_collapses_sign():
    """Проверяет, что resolve_unary сворачивает знак и число в один токен."""
    tokens = tokenize("5 * -3")
    resolved = resolve_unary(tokens)
    assert resolved == [("digit", 5.0), ("operator", "*"), ("digit", -3.0)]


# --- Негативные тесты ---

def test_empty_expression_raises():
    """Проверяет, что пустое выражение вызывает ошибку."""
    with pytest.raises(EmptyExpressionError):
        validate(tokenize(""))


def test_invalid_character_raises():
    """Проверяет, что недопустимый символ вызывает ошибку."""
    with pytest.raises(InvalidCharacterError):
        tokenize("2 & 2")


def test_trailing_operator_raises():
    """Проверяет, что выражение, заканчивающееся оператором, вызывает ошибку."""
    with pytest.raises(MissingNumError):
        validate(tokenize("5 -"))


def test_leading_binary_operator_raises():
    """Проверяет, что выражение, начинающееся с * или /, вызывает ошибку."""
    with pytest.raises(MissingNumError):
        validate(tokenize("* 5"))


def test_two_binary_operators_raise():
    """Проверяет, что два бинарных оператора подряд вызывают ошибку."""
    with pytest.raises(TwoBinaryOperatorsError):
        validate(tokenize("5 * * 3"))


def test_two_numbers_in_a_row_raise():
    """Проверяет, что два числа подряд без оператора вызывают ошибку."""
    with pytest.raises(MissingOperatorError):
        validate(tokenize("5 3"))


def test_division_by_zero_raises():
    """Проверяет, что деление на ноль вызывает ошибку."""
    with pytest.raises(DivisionByZeroError):
        run("5 / 0")
