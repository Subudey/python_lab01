# mypy: disable-error-code="arg-type"
"""Калькулятор, вычисляющий значение выражения."""

from .errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingNumError,
    MissingOperatorError,
    TwoBinaryOperatorsError,
)


def tokenize(expr: str) -> list:
    """Разбивает строку арифметического выражения на список токенов.

    Проходит по строке посимвольно, распознаёт числа,
    операторы +, -, *, / и игнорирует пробелы между токенами.

    Args:
        expr: исходная строка выражения.

    Returns:
        Список токенов, где каждый токен — кортеж вида ("digit", float)
        для чисел или ("operator", str) для операторов +, -, *, /.

    Raises:
        InvalidCharacterError: если в строке встретился символ, не
            являющийся цифрой, точкой, оператором или пробелом.
    """

    tokens = []
    i = 0

    while i < len(expr):
        if expr[i].isdigit():
            token = ""
            dot_cnt = 0

            while expr[i].isdigit() or expr[i] == ".":
                if expr[i] == '.':
                    dot_cnt += 1

                if dot_cnt > 1:
                    break

                token += expr[i]

                i += 1
                if i >= len(expr):
                    break

            tokens.append(("digit", float(token)))

        elif expr[i] in '+-*/':
            tokens.append(("operator", expr[i]))
            i += 1

        elif expr[i] == ' ':
            i += 1

        else:
            raise InvalidCharacterError("Неверный аргумент")

    return tokens


def validate(tokens: list) -> None:
    """Проверяет список токенов на корректность.

    Убеждается, что выражение не пустое, не начинается и не
    заканчивается недопустимым оператором, не содержит двух чисел или
    двух бинарных операторов подряд.

    Args:
        tokens: список токенов арифметического выражения.

    Raises:
        EmptyExpressionError: если список токенов пуст.
        MissingNumError: если выражение начинается или заканчивается
            оператором без числа на нужном месте.
        TwoBinaryOperatorsError: если два бинарных оператора идут
            подряд без допустимого унарного знака между ними.
        MissingOperatorError: если два числа идут подряд без
            оператора между ними.
    """

    if not tokens:
        raise EmptyExpressionError("Пустое выражение")

    if tokens[-1][0] == 'operator':
        raise MissingNumError("Пропущенное число в конце выражения")

    first = tokens[0]
    if first[0] == 'operator':

        if first[1] in '*/':
            raise MissingNumError("Пропущенное число в начале выражения")

        else:
            if len(tokens) == 1 or tokens[1][0] == 'operator':
                raise TwoBinaryOperatorsError("Два бинарных оператора подряд")

    for i in range(len(tokens) - 1):
        if tokens[i][0] == 'digit' and tokens[i + 1][0] == 'digit':
            raise MissingOperatorError("Пропущенный оператор")

        elif tokens[i][0] == 'operator' and tokens[i + 1][0] == 'operator':
            is_unary = (
                    tokens[i + 1][1] in '+-'
                    and i + 2 < len(tokens)
                    and tokens[i + 2][0] == 'digit'
            )

            if not is_unary:
                raise TwoBinaryOperatorsError("Два бинарных оператора подряд")


def resolve_unary(tokens: list) -> list:
    """Сворачивает унарные + и - вместе со следующим числом.

    Проходит по списку токенов и там, где + или - стоит в позиции
    унарного знака, заменяет пару "знак" и "число" на одно число с уже
    применённым знаком.

    Args:
        tokens: список токенов, прошедший проверку validate.

    Returns:
        Новый список токенов без унарных операторов: только числа и
        бинарные операторы.
    """

    result = []

    i = 0
    while i < len(tokens):
        if tokens[i][0] == 'digit':
            result.append(tokens[i])
            i += 1

        else:
            if tokens[i][1] in '*/':
                result.append(tokens[i])
                i += 1

            else:
                if i == 0 or result[-1][0] == 'operator':
                    result.append(('digit', -tokens[i + 1][1] if tokens[i][1] == '-' else tokens[i + 1][1]))
                    i += 2

                else:
                    result.append(tokens[i])
                    i += 1

    return result


def calculate(tokens: list) -> float:
    """Вычисляет значение арифметического выражения по списку токенов.

    Сначала разрешает унарные знаки через resolve_unary, затем
    сворачивает выражение в два прохода: сначала все операции
    умножения и деления слева направо, затем оставшиеся сложение и
    вычитание, соблюдая приоритет операций.

    Args:
        tokens: список токенов, прошедший проверку validate.

    Returns:
        Результат вычисления выражения.

    Raises:
        DivisionByZeroError: если в выражении встретилось деление на ноль.
    """

    tokens = resolve_unary(tokens)
    apply_priority_operators = []

    i = 0
    while i < len(tokens):
        if tokens[i][0] == 'digit':
            accumulation = tokens[i][1]
            j = i + 1

            while j < len(tokens) and tokens[j][0] == 'operator' and tokens[j][1] in '*/':
                operator = tokens[j][1]
                digit = tokens[j + 1][1]

                if operator == '/' and digit == 0:
                    raise DivisionByZeroError("Деление на ноль")

                accumulation = (accumulation * digit if operator == '*'
                                else accumulation / digit)
                j += 2

            apply_priority_operators.append(('digit', accumulation))
            i = j

        else:
            apply_priority_operators.append(tokens[i])
            i += 1

    result = apply_priority_operators[0][1]
    for i in range(1, len(apply_priority_operators) - 1, 2):
        operator = apply_priority_operators[i][1]
        digit = apply_priority_operators[i + 1][1]

        result = (result + digit if operator == '+'
                  else result - digit)

    return result
