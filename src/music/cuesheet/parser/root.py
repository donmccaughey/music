from music.cuesheet.lexer.token import Token

from .node import Node


class Root(Node):
    def __init__(self, children: list[Node]):
        super().__init__([], children)
