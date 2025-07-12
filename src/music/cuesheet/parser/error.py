from typing import Self

from music.cuesheet.lexer.token import Token

from .node import Node


class Error(Node):
    def __init__(self, line_num: int):
        super().__init__([], [])
        self.line_num = line_num

    @property
    def value(self):
        source = ' '.join([str(token.value) for token in self.tokens])
        return f'{self.line_num}: {source}'

    @classmethod
    def from_line(cls, tokens: list[Token]) -> Self:
        line_num = tokens[0].line_num if tokens else 0
        error = cls(line_num)
        error.tokens = tokens
        return error
