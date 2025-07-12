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

    type_pattern = [
        TokenType.NAME,
        TokenType.NAME,
        TokenType.INT,
        TokenType.EOL,
    ]

    @classmethod
    def is_year(cls, tokens: list[Token]) -> bool:
        return (
            [token.type for token in tokens] == cls.type_pattern
            and tokens[0].value == 'REM'
            and tokens[1].value == 'YEAR'
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_year(tokens) else None
