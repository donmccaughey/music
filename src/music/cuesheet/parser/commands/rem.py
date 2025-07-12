from typing import Self

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from music.cuesheet.parser.node import Node


class Rem(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])
        self.value = ' '.join([str(token.value) for token in tokens])

    @classmethod
    def is_rem(cls, tokens: list[Token]) -> bool:
        return (
            len(tokens) >= 2
            and tokens[0].type == TokenType.NAME
            and tokens[0].value == 'REM'
            and tokens[-1].type == TokenType.EOL
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_rem(tokens) else None
