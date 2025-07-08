from music.cuesheet.lexer.token import Token

from .node import Node


class Year(Node):
    def __init__(self, tokens: list[Token]):
        assert len(tokens) == 1
        assert isinstance(tokens[0].value, int)
        super().__init__(tokens, [])
        self.value = tokens[0].value
