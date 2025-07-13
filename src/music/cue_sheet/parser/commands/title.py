from typing import Self

from music.cue_sheet.lexer import EOL, NAME, QSTR, Token, types_of

from music.cue_sheet.parser.node import Node


class Title(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])

        assert isinstance(tokens[1].value, str)
        self.value = tokens[1].value

    @classmethod
    def is_title(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, QSTR] == types_of(tokens)
            and 'TITLE' == tokens[0].value
        )  # fmt: skip

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_title(tokens) else None
