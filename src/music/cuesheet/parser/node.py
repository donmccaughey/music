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

    def __repr__(self) -> str:
        lines: list[str] = []
        self._formatted_repr(depth=0, lines=lines)
        return '\n'.join(lines)

    def _formatted_repr(self, depth: int, lines: list[str]):
        indent = '    '
        lines.append(f'{indent * depth}{self.__class__.__name__}(')
        depth += 1
        lines.append(f'{indent * depth}tokens={self.tokens!r},')
        if self.children:
            lines.append(f'{indent * depth}children=[')
            depth += 1
            for child in self.children:
                child._formatted_repr(depth, lines)
            depth -= 1
        else:
            lines.append(f'{indent * depth}children=[]')
        lines.append(f'{indent * depth}],')
        depth -= 1
        lines.append(f'{indent * depth})')
