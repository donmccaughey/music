from music.cuesheet.lexer.token import Token

from .node import Node


class Rem(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])
        self.value = ' '.join([str(token.value) for token in tokens])
