from itertools import filterfalse as filter_out
from typing import Generator, Iterator

from .token import Token
from .token_type import TokenType


def take_line(token_iter: Iterator[Token]) -> Generator[list[Token]]:
    tokens: list[Token] = []
    no_ws_iter = filter_out(lambda token: token.is_whitespace, token_iter)
    while token := next(no_ws_iter, None):
        if token.is_end_of_line:
            yield tokens
        else:
            tokens.append(token)
    if tokens:
        yield tokens


def take_non_blank_line(token_iter: Iterator[Token]) -> list[Token] | None:
    non_blank_lines = filter_out(
        lambda tokens: tokens == [], take_line(token_iter)
    )
    return next(non_blank_lines, None)


def types_of(tokens: list[Token]) -> list[TokenType]:
    return [token.type for token in tokens]
