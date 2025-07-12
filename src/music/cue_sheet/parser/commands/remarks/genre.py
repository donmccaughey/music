from typing import Self

from music.cue_sheet.lexer import Token, TokenType

from music.cue_sheet.parser.node import Node


class Genre(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        assert isinstance(tokens[2].value, str)
        self.value = tokens[2].value

    type_pattern = [
        TokenType.NAME,
        TokenType.NAME,
        TokenType.QSTR,
        TokenType.EOL,
    ]

    @classmethod
    def is_genre(cls, tokens: list[Token]) -> bool:
        return (
            [token.type for token in tokens] == cls.type_pattern
            and tokens[0].value == 'REM'
            and tokens[1].value == 'GENRE'
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_genre(tokens) else None
