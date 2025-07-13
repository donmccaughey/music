from typing import Self

from music.cue_sheet.lexer import EOL, INT, NAME, Token, types_of
from music.cue_sheet.parser.node import Node


class Year(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])

        assert isinstance(tokens[2].value, int)
        self.value = tokens[2].value

    @classmethod
    def is_year(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, NAME, INT] == types_of(tokens)
            and 'REM' == tokens[0].value
            and 'YEAR' == tokens[1].value
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_year(tokens) else None
