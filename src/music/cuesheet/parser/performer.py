from typing import Self

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class Performer(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        assert isinstance(tokens[1].value, str)
        self.value = tokens[1].value

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        types = [t.type for t in tokens]
        if [TokenType.NAME, TokenType.QSTR, TokenType.EOL] == types:
            return cls(tokens)
        else:
            return None
