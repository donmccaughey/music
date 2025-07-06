from music.cuesheet.lexer.token import Token

from .node import Node


class Track(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        super().__init__(tokens, children)
