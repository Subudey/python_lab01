"""Хранит константы необходимые для работы программы."""
import json
import re
from pathlib import Path

NUMBER_PATTERN = re.compile(r"\d+\.?\d*")

CONFIG_PATH = Path(__file__).parent.parent / "resources" / "units_config.json"
_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
LENGTH_UNITS = _config["length"]
MASS_UNITS = _config["mass"]
TEMPERATURE_UNITS = set(_config["temperature"])

HISTORY_PATH = Path(__file__).parent.parent / "resources" / "history.json"
