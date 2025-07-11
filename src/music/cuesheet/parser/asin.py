from music.cuesheet.lexer.token import Token

from .node import Node


class ASIN(Node):
    def __init__(self, tokens: list[Token]):
        assert len(tokens) == 4
        assert isinstance(tokens[2].value, str)
        super().__init__(tokens, [])
        self.value = tokens[2].value
