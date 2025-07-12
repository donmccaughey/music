from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from music.cue_sheet.lexer.line import Line

from .command import Command
from .split import split_quoted_string


@dataclass
class Performer(Command):
    name: str

    @classmethod
    def parse(cls, line: Line) -> Self | None:
        name = split_quoted_string('PERFORMER', line.line)
        return cls(line, name) if name else None
