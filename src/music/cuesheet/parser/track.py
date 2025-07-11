from typing import Self

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class Track(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        super().__init__(tokens, children)

        assert isinstance(tokens[1].value, int)
        self.number = tokens[1].value

        assert isinstance(tokens[2].value, str)
        self.type = tokens[2].value

    type_pattern = [
        TokenType.NAME,
        TokenType.INT,
        TokenType.NAME,
        TokenType.EOL,
    ]

    @classmethod
    def is_track(cls, tokens: list[Token]) -> bool:
        types = [tokens.type for tokens in tokens]
        return types == cls.type_pattern and tokens[2].value in ['AUDIO']

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens, children=[]) if cls.is_track(tokens) else None
