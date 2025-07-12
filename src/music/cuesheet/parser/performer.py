from typing import Self

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class Performer(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        assert isinstance(tokens[1].value, str)
        self.value = tokens[1].value

    type_pattern = [TokenType.NAME, TokenType.QSTR, TokenType.EOL]

    @classmethod
    def is_performer(cls, tokens: list[Token]) -> bool:
        types = [tokens.type for tokens in tokens]
        return types == cls.type_pattern and tokens[0].value == 'PERFORMER'

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_performer(tokens) else None
