from dataclasses import dataclass

from music.cuesheet.lexer.token import Token

from .node import Node


@dataclass
class Command(Node):
    tokens: list[Token]
