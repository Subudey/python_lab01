"""Иерархия исключений для калькулятора и конвертера величин."""

class ToolkitError(Exception):
    """Базовый класс для всех ошибок пакета toolkit."""


class CalculatorError(ToolkitError):
    """Базовый класс для ошибок, возникающих при работе калькулятора."""

class ConverterError(ToolkitError):
    """Выражение для вычисления оказалось пустым."""


class EmptyExpressionError(CalculatorError):
    """В выражении встретился недопустимый символ."""

class InvalidCharacterError(CalculatorError):
    """В выражении пропущено число там, где оно обязательно."""

class MissingOperatorError(CalculatorError):
    """Между двумя числами пропущен оператор."""

class MissingNumError(CalculatorError):
    """В выражении пропущено число"""

class TwoBinaryOperatorsError(CalculatorError):
    """В выражении два бинарных оператора идут подряд."""

class DivisionByZeroError(CalculatorError):
    """Попытка деления на ноль."""


class UnknownUnitError(ConverterError):
    """Единица измерения не найдена ни в одной известной группе."""

class IncompatibleUnitsError(ConverterError):
    """Единицы измерения принадлежат разным группам."""

class BelowAbsoluteZeroError(ConverterError):
    """Результат перевода температуры оказался ниже абсолютного нуля."""
