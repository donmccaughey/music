from music.cue_sheet.lexer import Token

from .node import Node


class Error(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, children=[])

        self.line_num = tokens[0].line_num if tokens else 0
        self.value = ' '.join([str(token.value) for token in tokens])
