from __future__ import annotations

from dataclasses import dataclass

from music.cuesheet.lexer.token import Token


@dataclass
class Node:
    tokens: list[Token]
    children: list[Node]
