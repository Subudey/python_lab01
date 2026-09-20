
"""Конвертация величин между единицами измерения длины, массы и температуры."""

from .constants import LENGTH_UNITS, MASS_UNITS, TEMPERATURE_UNITS
from .errors import BelowAbsoluteZeroError, IncompatibleUnitsError, UnknownUnitError


def get_group(unit: str) -> str:
    """Определяет группу величин, к которой относится единица измерения.

    Args:
        unit: название единицы измерения в нижнем регистре.

    Returns:
        Название группы.

    Raises:
        UnknownUnitError: если единица не найдена ни в одной группе.
    """

    if unit in LENGTH_UNITS:
        return 'length'

    elif unit in MASS_UNITS:
        return 'mass'

    elif unit in TEMPERATURE_UNITS:
        return 'temperature'

    else:
        raise UnknownUnitError("Неизвестная группа")



def convert(value: float, unit_from: str, unit_to: str) -> float:
    """Переводит значение из одной единицы измерения в другую.

    Для длины и массы используется линейный пересчёт через базовую
    единицу группы; для температуры — явные формулы пересчёта через
    Кельвины.

    Args:
        value: исходное числовое значение.
        unit_from: единица измерения, из которой переводим.
        unit_to: единица измерения, в которую переводим.

    Returns:
        Значение value, выраженное в unit_to.

    Raises:
        UnknownUnitError: если unit_from или unit_to не известны.
        IncompatibleUnitsError: если unit_from и unit_to принадлежат разным группам величин.
        BelowAbsoluteZeroError: если результат перевода температуры в Кельвины получается отрицательным.
    """

    unit_from = unit_from.lower()
    unit_to = unit_to.lower()

    group_from = get_group(unit_from)
    group_to = get_group(unit_to)

    if group_from != group_to:
        raise IncompatibleUnitsError("Несовместимые группы для конвертации")

    if group_from == 'length':
        return (LENGTH_UNITS[unit_from] / LENGTH_UNITS[unit_to]) * value

    elif group_from == 'mass':
        return (MASS_UNITS[unit_from] / MASS_UNITS[unit_to]) * value

    else:
        if unit_from == 'c':
            kelvin = value + 273.15

        elif unit_from == 'f':
            kelvin = (value - 32) * 5/9 + 273.15

        else:
            kelvin = value


        if kelvin < 0:
            raise BelowAbsoluteZeroError("negative kelvin")


        if unit_to == 'c':
            return kelvin - 273.15

        elif unit_to == 'f':
            return (kelvin - 273.15) * 9/5 + 32

        else:
            return kelvin
