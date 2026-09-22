"""Точка входа CLI для пакета toolkit: калькулятор и конвертер величин."""

import argparse
import sys

from .calculator import calculate, tokenize, validate
from .converter import convert
from .errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Собирает парсер аргументов командной строки для toolkit."""

    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Консольный набор инструментов: калькулятор арифметических выражений и конвертер величин",
        epilog=(
            "Примеры:\n"
            '  python -m toolkit calc "2 + 3 * 4"\n'
            '  python -m toolkit calc "-5 / 2"\n\n'
            "  python -m toolkit convert 100 --from cm --to m\n"
            "  python -m toolkit convert 20 --from c --to f"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    calc_parser = subparsers.add_parser(
        "calc",
        help="Находит значение арифметического выражения",
    )
    calc_parser.add_argument("expression")

    convert_parser = subparsers.add_parser(
        "convert",
        help="Конвертирует значение между разными единицами измерения",
    )
    convert_parser.add_argument("value", type=float)
    convert_parser.add_argument("--from", dest="unit_from", required=True)
    convert_parser.add_argument("--to", dest="unit_to", required=True)

    return parser


def main() -> None:
    """Точка входа CLI: разбирает аргументы и запускает нужную команду."""

    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "calc":
            tokens = tokenize(args.expression)
            validate(tokens)
            result = calculate(tokens)
            print(result)

        elif args.command == "convert":
            result = convert(args.value, args.unit_from, args.unit_to)
            print(result)

        else:
            parser.print_help()
            sys.exit(2)

    except ToolkitError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
