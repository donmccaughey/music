from __future__ import annotations

from typing import Any

from music.cuesheet.lexer.token import Token


class Node:
    def __init__(self, tokens: list[Token], children: list[Node]):
        self.tokens = tokens
        self.children = children

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Node):
            return (
                self.tokens == other.tokens and self.children == other.children
            )
        else:
            return NotImplemented
