from typing import Self

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class Year(Node):
    def __init__(self, tokens: list[Token]):
        assert len(tokens) == 4
        assert isinstance(tokens[2].value, int)
        super().__init__(tokens, [])
        self.value = tokens[2].value

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.NAME,
            TokenType.INT,
            TokenType.EOL,
        ] == types:
            return cls(tokens)
        else:
            return None
