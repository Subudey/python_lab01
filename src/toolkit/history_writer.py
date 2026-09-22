import json

from .constants import HISTORY_PATH


def save_to_history(expr: str, result: float) -> None:
    """Добавляет запись об успешном выполнении в файл с историей

    Создает папку src/resources и в ней файл history.json если такого не было и
    помещает в него выражение с результатом

    Args:
        expr: выражение для сохранения
        result: результат выражения expr
    """

    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    if HISTORY_PATH.exists():
        history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))

    else:
        history = []

    history.append({"expression": expr, "result": result})
    HISTORY_PATH.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
