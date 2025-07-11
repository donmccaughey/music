from pathlib import Path
from typing import Self

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class File(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        super().__init__(tokens, children)

        assert isinstance(tokens[1].value, str)
        self.filename = Path(tokens[1].value)

        assert isinstance(tokens[2].value, str)
        self.type = tokens[2].value

    type_pattern = [
        TokenType.NAME,
        TokenType.QSTR,
        TokenType.NAME,
        TokenType.EOL,
    ]

    @classmethod
    def is_file(cls, tokens: list[Token]) -> bool:
        types = [token.type for token in tokens]
        return types == cls.type_pattern and tokens[2].value in ['WAVE']

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens, children=[]) if cls.is_file(tokens) else None
