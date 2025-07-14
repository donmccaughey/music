from typing import Generator, Iterator

from .token import Token
from .token_type import TokenType


def take_lines(token_iter: Iterator[Token]) -> Generator[list[Token]]:
    tokens: list[Token] = []
    for token in token_iter:
        if token.is_end_of_line:
            yield tokens
            tokens = []
        else:
            tokens.append(token)
    if tokens:
        yield tokens


def take_non_blank_lines(token_iter: Iterator[Token]) -> Generator[list[Token]]:
    no_ws_iter = filter(lambda token: not token.is_whitespace, token_iter)
    yield from filter(lambda line: len(line), take_lines(no_ws_iter))


def types_of(tokens: list[Token]) -> list[TokenType]:
    return [token.type for token in tokens]
