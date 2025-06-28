from __future__ import annotations

from dataclasses import dataclass

from .command import Command
from .split import split_quoted_string


@dataclass
class Performer(Command):
    name: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Performer | None:
        name = split_quoted_string('PERFORMER', line)
        return cls(line_number, line, name) if name else None
