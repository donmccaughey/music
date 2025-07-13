from typing import Self

from music.cue_sheet.lexer import EOL, NAME, STR, Token
from music.cue_sheet.parser.node import Node


class DiscID(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])

        assert isinstance(tokens[2].value, str)
        self.value = tokens[2].value

    type_pattern = [NAME, NAME, STR, EOL]

    @classmethod
    def is_disk_id(cls, tokens: list[Token]) -> bool:
        return (
            [token.type for token in tokens] == cls.type_pattern
            and tokens[0].value == 'REM'
            and tokens[1].value == 'DISCID'
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_disk_id(tokens) else None
