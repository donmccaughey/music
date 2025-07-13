from typing import Self

from music.cue_sheet import IndexPoint
from music.cue_sheet.lexer import EOL, IDX_PT, INT, NAME, Token, types_of

from music.cue_sheet.parser.node import Node


class Index(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])

        assert isinstance(tokens[1].value, int)
        self.number = tokens[1].value

        assert isinstance(tokens[2].value, IndexPoint)
        self.index_point = tokens[2].value

    @classmethod
    def is_index(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, INT, IDX_PT] == types_of(tokens)
            and 'INDEX' == tokens[0].value
        )  # fmt: skip

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens) if cls.is_index(tokens) else None
