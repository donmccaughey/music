from music.cuesheet.lexer.token import Token

from .node import Node


class Track(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        assert len(tokens) == 2
        assert isinstance(tokens[0].value, int)
        assert isinstance(tokens[1].value, str)
        super().__init__(tokens, children)
        self.number = tokens[0].value
        self.type = tokens[1].value
