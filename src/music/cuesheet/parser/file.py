from pathlib import Path

from music.cuesheet.lexer.token import Token

from .node import Node


class File(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        assert len(tokens) == 2
        assert isinstance(tokens[0].value, str)
        assert isinstance(tokens[1].value, str)
        super().__init__(tokens, children)
        self.filename = Path(tokens[0].value)
        self.type = tokens[1].value
