from pathlib import Path
from typing import Self

from music.cue_sheet.lexer import EOL, NAME, QSTR, Token, types_of

from music.cue_sheet.parser.node import Node


class File(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        super().__init__(tokens, children)

        assert isinstance(tokens[1].value, str)
        self.filename = Path(tokens[1].value)

        if 2 == len(tokens):
            self.type = 'WAVE'
        else:
            assert isinstance(tokens[2].value, str)
            self.type = tokens[2].value

    @classmethod
    def is_file(cls, tokens: list[Token]) -> bool:
        return cls.is_file_with_type(tokens) or cls.is_file_without_type(tokens)

    @classmethod
    def is_file_with_type(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, QSTR, NAME] == types_of(tokens)
            and 'FILE' == tokens[0].value
            and tokens[2].value in ['WAVE']
        )

    @classmethod
    def is_file_without_type(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, QSTR] == types_of(tokens)
            and 'FILE' == tokens[0].value
        )  # fmt: skip

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens, children=[]) if cls.is_file(tokens) else None
