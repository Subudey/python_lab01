from toolkit.errors import DivisionByZeroError


def resolve_unary(tokens: list) -> list:
    """Сворачивает цепочку унарных + и - вместе со следующим числом.

    Там, где подряд идёт один или несколько унарных знаков, вычисляет
    их суммарный знак (чётное число минусов даёт плюс, нечётное —
    минус) и применяет его к идущему следом числу.

    Args:
        tokens: список токенов, прошедший проверку validate.

    Returns:
        Новый список токенов без унарных операторов: только числа и
        бинарные операторы.
    """

    result = []
    i = 0

    while i < len(tokens):
        kind, value = tokens[i]

        if kind == 'digit' or value in '*/':
            result.append(tokens[i])
            i += 1

        else:
            if i == 0 or result[-1][0] == 'operator':
                sign = 1
                while i < len(tokens) and tokens[i][0] == 'operator' and tokens[i][1] in '+-':
                    if tokens[i][1] == '-':
                        sign *= -1
                    i += 1

                number = float(tokens[i][1])
                result.append(('digit', str(sign * number)))
                i += 1

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
            accumulation = float(tokens[i][1])
            j = i + 1

            while j < len(tokens) and tokens[j][0] == 'operator' and tokens[j][1] in '*/':
                operator = tokens[j][1]
                digit = float(tokens[j + 1][1])

                if operator == '/' and digit == 0:
                    raise DivisionByZeroError("Деление на ноль")

                accumulation = (accumulation * digit if operator == '*'
                                else accumulation / digit)
                j += 2

            apply_priority_operators.append(('digit', str(accumulation)))
            i = j

        else:
            apply_priority_operators.append(tokens[i])
            i += 1

    result = float(apply_priority_operators[0][1])

    for i in range(1, len(apply_priority_operators) - 1, 2):
        operator = apply_priority_operators[i][1]
        digit = float(apply_priority_operators[i + 1][1])

        result = (result + digit if operator == '+'
                  else result - digit)

    return result
