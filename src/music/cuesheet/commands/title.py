from __future__ import annotations

from dataclasses import dataclass

from .command import Command
from .split import split_quoted_string


@dataclass
class Title(Command):
    title: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Title | None:
        name = split_quoted_string('TITLE', line)
        return Title(line_number, line, name) if name else None
