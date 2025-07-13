from itertools import filterfalse as filter_out
from typing import Iterator

from . import TokenType
from .token import Token
from .token_type import EOL


def chomp(tokens: list[Token]) -> list[Token]:
    if tokens and tokens[-1].type == EOL:
        return tokens[:-1]
    else:
        return tokens


def is_blank_line(tokens: list[Token]) -> bool:
    return 1 == len(tokens) and EOL == tokens[0].type


def take_line(token_iter: Iterator[Token]) -> list[Token]:
    tokens = []
    no_ws_iter = filter_out(lambda token: token.is_whitespace, token_iter)
    while token := next(no_ws_iter, None):
        tokens.append(token)
        if token.is_end_of_line:
            break
    return tokens


def take_non_blank_line(token_iter: Iterator[Token]) -> list[Token]:
    while True:
        tokens = take_line(token_iter)
        if not is_blank_line(tokens):
            return tokens


def types_of(tokens: list[Token]) -> list[TokenType]:
    return [token.type for token in tokens]
