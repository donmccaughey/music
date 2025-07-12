from typing import Self

from music.cue_sheet.lexer.token import Token
from music.cue_sheet.lexer.token_type import TokenType
from music.cue_sheet.lexer.tokens import chomp

from music.cue_sheet.parser.node import Node


class Rem(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])
        self.value = ' '.join([str(token.value) for token in chomp(tokens[1:])])

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
