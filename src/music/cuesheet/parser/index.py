from typing import Self

from music.cuesheet import IndexPoint
from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class Index(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        assert isinstance(tokens[1].value, int)
        self.number = tokens[1].value

        assert isinstance(tokens[2].value, IndexPoint)
        self.index_point = tokens[2].value

    type_pattern = [
        TokenType.NAME,
        TokenType.INT,
        TokenType.IDX_PT,
        TokenType.EOL,
    ]

    @classmethod
    def is_index(cls, tokens: list[Token]) -> bool:
        types = [token.type for token in tokens]
        return types == cls.type_pattern

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_index(tokens) else None
