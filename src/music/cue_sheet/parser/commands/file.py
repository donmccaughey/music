from pathlib import Path
from typing import Self

from music.cue_sheet.lexer import Token, TokenType

from music.cue_sheet.parser.node import Node


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
        return (
            [token.type for token in tokens] == cls.type_pattern
            and tokens[0].value == 'FILE'
            and tokens[2].value in ['WAVE']
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens, children=[]) if cls.is_file(tokens) else None
