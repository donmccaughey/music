from music.cuesheet.lexer.token import Token

from .node import Node


class Performer(Node):
    def __init__(self, tokens: list[Token]):
        assert len(tokens) == 3
        assert isinstance(tokens[1].value, str)
        super().__init__(tokens, [])
        self.value = tokens[1].value
