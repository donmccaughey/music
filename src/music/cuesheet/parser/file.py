from pathlib import Path

from music.cuesheet.lexer.token import Token

from .node import Node


class File(Node):
    def __init__(self, tokens: list[Token], children: list[Node]):
        assert len(tokens) == 4
        assert isinstance(tokens[1].value, str)
        assert isinstance(tokens[2].value, str)
        super().__init__(tokens, children)
        self.filename = Path(tokens[1].value)
        self.type = tokens[2].value
