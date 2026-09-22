"""Таблицы коэффициентов и допустимых единиц измерения для конвертера, а также паттерн для tokenize."""
import re

LENGTH_UNITS = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
MASS_UNITS = {"g": 1.0, "kg": 1000.0}
TEMPERATURE_UNITS = {"c", "f", "k"}

NUMBER_PATTERN = re.compile(r"\d+\.?\d*")
