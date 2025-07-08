from music.cuesheet.lexer.token import Token

from .node import Node


class Error(Node):
    def __init__(self, tokens: list[Token]):
        assert tokens
        super().__init__(tokens, [])
        line = tokens[0].line
        source = ' '.join([str(token.value) for token in tokens])
        self.value = f'{line}: {source}'
