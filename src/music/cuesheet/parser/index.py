from music.cuesheet import IndexPoint
from music.cuesheet.lexer.token import Token

from .node import Node


class Index(Node):
    def __init__(self, tokens: list[Token]):
        assert len(tokens) == 2
        assert isinstance(tokens[0].value, int)
        assert isinstance(tokens[1].value, IndexPoint)
        super().__init__(tokens, [])
        self.number = tokens[0].value
        self.index_point = tokens[1].value
