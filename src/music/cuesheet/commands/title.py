from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from .command import Command
from .lines import Line
from .split import split_quoted_string


@dataclass
class Title(Command):
    title: str

    @classmethod
    def parse(cls, line: Line) -> Self | None:
        name = split_quoted_string('TITLE', line.line)
        return cls(line.line_number, line.line, name) if name else None
