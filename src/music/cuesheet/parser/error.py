from music.cuesheet.lexer.token import Token

from .node import Node


class Error(Node):
    def __init__(self, line: int):
        super().__init__([], [])
        self.line = line

    @property
    def value(self):
        source = ' '.join([str(token.value) for token in self.tokens])
        return f'{self.line}: {source}'
