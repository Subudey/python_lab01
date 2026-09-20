"""Тесты для конвертера величин: convert, get_group."""

import pytest

from toolkit.converter import convert, get_group
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)

# --- Позитивные тесты ---

def test_length_conversion():
    """Проверяет конвертацию сантиметров в метры."""
    assert convert(100, "cm", "m") == 1.0


def test_mass_conversion():
    """Проверяет конвертацию килограммов в граммы."""
    assert convert(2, "kg", "g") == 2000.0


def test_temperature_c_to_k():
    """Проверяет конвертацию Цельсия в Кельвины."""
    assert convert(0, "c", "k") == 273.15


def test_temperature_f_to_c():
    """Проверяет конвертацию Фаренгейта в Цельсий."""
    assert convert(32, "f", "c") == 0.0


def test_unit_case_insensitive():
    """Проверяет, что регистр единиц измерения не учитывается."""
    assert convert(5, "KM", "m") == convert(5, "km", "m")


def test_get_group_length():
    """Проверяет определение группы для единицы длины."""
    assert get_group("km") == "length"


# --- Негативные тесты ---

def test_unknown_unit_raises():
    """Проверяет, что неизвестная единица измерения вызывает ошибку."""
    with pytest.raises(UnknownUnitError):
        convert(5, "banana", "m")


def test_incompatible_units_raise():
    """Проверяет, что конвертация между разными группами вызывает ошибку."""
    with pytest.raises(IncompatibleUnitsError):
        convert(5, "km", "kg")


def test_below_absolute_zero_raises():
    """Проверяет, что температура ниже абсолютного нуля вызывает ошибку."""
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-300, "c", "k")
