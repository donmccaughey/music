from music.cuesheet.lexer.token import Token

from .node import Node


class Year(Node):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens, [])
