from typing import Self

from music.cue_sheet.lexer import EOL, INT, NAME, Token

from music.cue_sheet.parser.node import Node


class Track(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        super().__init__(tokens, children)

        assert isinstance(tokens[1].value, int)
        self.number = tokens[1].value

        assert isinstance(tokens[2].value, str)
        self.type = tokens[2].value

    type_pattern = [NAME, INT, NAME, EOL]

    @classmethod
    def is_track(cls, tokens: list[Token]) -> bool:
        return (
            [tokens.type for tokens in tokens] == cls.type_pattern
            and tokens[0].value == 'TRACK'
            and tokens[2].value in ['AUDIO']
        )

    @classmethod
    def parse(cls, tokens: list[Token]) -> Self | None:
        return cls(tokens, children=[]) if cls.is_track(tokens) else None
