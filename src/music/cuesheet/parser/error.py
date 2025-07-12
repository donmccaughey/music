from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.tokens import chomp

from music.cuesheet.parser.node import Node


class Error(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])

        self.line_num = tokens[0].line_num if tokens else 0
        self.value = ' '.join([str(token.value) for token in chomp(tokens)])
