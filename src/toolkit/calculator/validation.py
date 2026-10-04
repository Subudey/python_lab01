from toolkit.errors import (
    EmptyExpressionError,
    MissingNumError,
    MissingOperatorError,
    TwoBinaryOperatorsError,
)


def validate(tokens: list) -> None:
    """Проверяет список токенов на корректность.

    Использует модель "предыдущий токен": унарные + и - допустимы в
    любом количестве подряд (в начале выражения, после числа как
    бинарный знак, после другого оператора как очередной унарный).
    Операторы * и / допустимы только сразу после числа.

    Args:
        tokens: список токенов арифметического выражения.

    Raises:
        EmptyExpressionError: если список токенов пуст.
        MissingNumError: если операнд ожидался, но его нет — в начале,
            перед * или / без предшествующего числа, либо в конце
            выражения.
        TwoBinaryOperatorsError: если оператор * или / идёт сразу
            после другого оператора.
        MissingOperatorError: если два числа идут подряд без
            оператора между ними.
    """

    if not tokens:
        raise EmptyExpressionError("Пустое выражение")

    prev = None

    for kind, value in tokens:
        if kind == 'digit':
            if prev == 'digit':
                raise MissingOperatorError("Пропущенный оператор")
            prev = 'digit'

        else:
            if value in '+-':
                prev = 'operator'
            else:
                if prev is None:
                    raise MissingNumError("Пропущенное число в начале выражения")
                if prev == 'operator':
                    raise TwoBinaryOperatorsError("Два бинарных оператора подряд")
                prev = 'operator'

    if prev == 'operator':
        raise MissingNumError("Пропущенное число в конце выражения")
