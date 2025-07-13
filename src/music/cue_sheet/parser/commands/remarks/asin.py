from typing import Self

from music.cue_sheet.lexer import EOL, NAME, STR, Token, types_of
from music.cue_sheet.parser.node import Node


class ASIN(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])

        assert isinstance(tokens[2].value, str)
        self.value = tokens[2].value

    @classmethod
    def is_asin(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, NAME, STR, EOL] == types_of(tokens)
            and 'REM' == tokens[0].value
            and 'ASIN' == tokens[1].value
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_asin(tokens) else None
