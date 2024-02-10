from dataclasses import dataclass
from typing import Optional

from .command import Command
from .split import split_quoted_string


@dataclass
class Title(Command):
    title: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Title']:
        name = split_quoted_string('TITLE', line)
        return Title(line_number, line, name) if name else None
