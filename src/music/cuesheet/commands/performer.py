from dataclasses import dataclass
from typing import Optional

from .command import Command
from .split import split_quoted_string


@dataclass
class Performer(Command):
    name: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Performer']:
        name = split_quoted_string('PERFORMER', line)
        return Performer(line_number, line, name) if name else None
