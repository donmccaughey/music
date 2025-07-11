from music.cuesheet.lexer.token import Token

from .node import Node


class Error(Node):
    def __init__(self, line_num: int):
        super().__init__([], [])
        self.line_num = line_num

    @property
    def value(self):
        source = ' '.join([str(token.value) for token in self.tokens])
        return f'{self.line_num}: {source}'
