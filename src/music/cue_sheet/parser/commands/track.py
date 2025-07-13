from typing import Self

from music.cue_sheet.lexer import EOL, INT, NAME, Token, types_of

from music.cue_sheet.parser.node import Node


class Track(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        super().__init__(tokens, children)

        assert isinstance(tokens[1].value, int)
        self.number = tokens[1].value

        assert isinstance(tokens[2].value, str)
        self.type = tokens[2].value

    @classmethod
    def is_track(cls, tokens: list[Token]) -> bool:
        return (
            [NAME, INT, NAME, EOL] == types_of(tokens)
            and 'TRACK' == tokens[0].value
            and tokens[2].value in ['AUDIO']
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens, children=[]) if cls.is_track(tokens) else None
