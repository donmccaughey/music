from typing import Self

from music.cue_sheet.lexer import chomp, EOL, NAME, Token
from music.cue_sheet.parser.node import Node


class Rem(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])
        self.value = ' '.join([str(token.value) for token in chomp(tokens[1:])])

    @classmethod
    def is_rem(cls, tokens: list[Token]) -> bool:
        return (
            len(tokens) >= 2
            and tokens[0].type == NAME
            and tokens[0].value == 'REM'
            and tokens[-1].type == EOL
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_rem(tokens) else None
