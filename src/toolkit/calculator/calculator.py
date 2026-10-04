from .calculation import calculate
from .tokenization import tokenize
from .validation import validate


def get_result(expr: str) -> float:
    tokens = tokenize(expr)
    validate(tokens)
    return calculate(tokens)
