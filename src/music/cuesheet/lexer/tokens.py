from itertools import filterfalse as filter_out
from typing import Iterator

from .token import Token
from .token_type import TokenType


def is_blank_line(tokens: list[Token]) -> bool:
    return 1 == len(tokens) and TokenType.EOL == tokens[0].type


def take_line(token_iter: Iterator[Token]) -> list[Token]:
    tokens = []
    no_ws_iter = filter_out(lambda token: token.is_whitespace, token_iter)
    while token := next(no_ws_iter, None):
        tokens.append(token)
        if token.is_end_of_line:
            break
    return tokens
