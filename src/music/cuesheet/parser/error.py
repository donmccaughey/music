from music.cuesheet.lexer.token import Token

from .node import Node


class Error(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        self.line_num = tokens[0].line_num if tokens else 0

        source = ' '.join([str(token.value) for token in self.tokens])
        self.value = f'{self.line_num}: {source}'
