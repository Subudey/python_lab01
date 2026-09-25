"""CLI-тесты: проверяют запуск пакета как процесса через python -m toolkit."""

import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Запускает toolkit как отдельный процесс и возвращает результат."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_calc_success():
    """Проверяет успешное выполнение команды calc через CLI."""
    result = run_cli("calc", "2 + 2")
    assert result.returncode == 0
    assert result.stdout.strip() == "4.0"


def test_cli_convert_success():
    """Проверяет успешное выполнение команды convert через CLI."""
    result = run_cli("convert", "100", "--from", "cm", "--to", "m")
    assert result.returncode == 0
    assert result.stdout.strip() == "1.0"


def test_cli_calc_error_exit_code():
    """Проверяет код возврата 2 и вывод в stderr при ошибке калькулятора."""
    result = run_cli("calc", "5 / 0")
    assert result.returncode == 2
    assert result.stderr.strip() != ""
    assert result.stdout.strip() == ""


def test_cli_convert_error_exit_code():
    """Проверяет код возврата 2 при ошибке конвертера."""
    result = run_cli("convert", "5", "--from", "km", "--to", "kg")
    assert result.returncode == 2
    assert result.stderr.strip() != ""
