from music.cuesheet.parser.node import Node


class Root(Node):
    def __init__(self, children: list[Node]):
        super().__init__([], children)
