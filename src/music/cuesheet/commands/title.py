from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from music.cuesheet.lexer.line import Line

from .command import Command
from .split import split_quoted_string


@dataclass
class Title(Command):
    title: str

    @classmethod
    def parse(cls, line: Line) -> Self | None:
        name = split_quoted_string('TITLE', line.line)
        return cls(line, name) if name else None
