from toolkit.constants import NUMBER_PATTERN
from toolkit.errors import InvalidCharacterError


def tokenize(expr: str) -> list:
    """Разбивает строку арифметического выражения на список токенов.

    Проходит по строке слева направо, на каждом шаге ищет либо
    оператор, либо пробел, либо число по регулярному выражению.
    Игнорирует пробелы между токенами.

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
        if expr[i] in '+-*/':
            tokens.append(("operator", expr[i]))
            i += 1
            continue

        if expr[i] == ' ':
            i += 1
            continue

        number_match = NUMBER_PATTERN.match(expr, i)
        if number_match:
            tokens.append(("digit", number_match.group()))
            i = number_match.end()
            continue

        raise InvalidCharacterError("Неверный аргумент")

    return tokens
