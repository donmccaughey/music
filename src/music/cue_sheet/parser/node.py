from __future__ import annotations

from typing import Any

from music.cue_sheet.lexer import Token


class Node:
    def __init__(self, tokens: list[Token], children: list[Node]):
        self.tokens = tokens
        self.children = children

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return (
                self.tokens == other.tokens and self.children == other.children
            )
        else:
            return NotImplemented

    def __repr__(self) -> str:
        lines: list[str] = []
        self._indented_representation(depth=0, lines=lines)
        return '\n'.join(lines)

    def _indented_representation(self, depth: int, lines: list[str]):
        indent = '    '
        lines.append(f'{indent * depth}{self.__class__.__name__}(')
        depth += 1
        lines.append(f'{indent * depth}tokens={self.tokens!r},')
        if self.children:
            lines.append(f'{indent * depth}children=[')
            depth += 1
            for child in self.children:
                child._indented_representation(depth, lines)
            depth -= 1
        else:
            lines.append(f'{indent * depth}children=[]')
        lines.append(f'{indent * depth}],')
        depth -= 1
        lines.append(f'{indent * depth})')
