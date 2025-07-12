from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .node import Node


class Error(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        self.line_num = tokens[0].line_num if tokens else 0
        self.value = self._make_value(self.line_num, tokens)

    @staticmethod
    def _make_value(line_num: int, tokens: list[Token]):
        if tokens and tokens[-1].type == TokenType.EOL:
            tokens = tokens[:-1]
        source = ' '.join([str(token.value) for token in tokens])
        return f'{line_num}: {source}'
