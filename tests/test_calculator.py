import pytest

from toolkit.calculator.calculator import get_result
from toolkit.calculator.tokenization import tokenize
from toolkit.calculator.validation import validate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingNumError,
    MissingOperatorError,
    TwoBinaryOperatorsError,
)

# --- Позитивные тесты ---

def test_simple_addition():
    """Проверяет базовое сложение."""
    assert get_result("2 + 2") == 4.0


def test_operator_priority():
    """Проверяет, что умножение выполняется раньше сложения."""
    assert get_result("2 + 3 * 4") == 14.0


def test_division():
    """Проверяет деление вещественных чисел."""
    assert get_result("10 / 4") == 2.5


def test_unary_minus_at_start():
    """Проверяет унарный минус в начале выражения."""
    assert get_result("-5 + 10") == 5.0


def test_unary_plus_after_operator():
    """Проверяет унарный плюс после бинарного оператора."""
    assert get_result("5 * +3") == 15.0


def test_unary_minus_after_operator():
    """Проверяет унарный минус после бинарного оператора."""
    assert get_result("5 * -3") == -15.0


def test_ignores_whitespace():
    """Проверяет, что пробелы между токенами игнорируются."""
    assert get_result("2+2") == get_result("2 + 2")


def test_float_numbers():
    """Проверяет работу с вещественными числами."""
    assert get_result("1.5 + 2.5") == 4.0


def test_chained_multiplication():
    """Проверяет цепочку из нескольких операций умножения."""
    assert get_result("2 * 3 * 4") == 24.0


def test_mixed_priority_expression():
    """Проверяет смешанное выражение с разными приоритетами."""
    assert get_result("10 - 2 * 3 + 4 / 2") == 6.0


def test_multiple_unary_operators():
    """Проверяет, что цепочка из нескольких унарных знаков работает."""
    assert get_result("5 - - 3") == 8.0
    assert get_result("5 - - - 3") == 2.0


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
        get_result("5 / 0")
