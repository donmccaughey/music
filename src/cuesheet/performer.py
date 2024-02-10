from dataclasses import dataclass
from typing import Optional
from .parse import parse_quoted_string
from .statement import Statement


@dataclass
class Performer(Statement):
    name: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Performer']:
        name = parse_quoted_string('PERFORMER', line)
        return Performer(line_number, line, name) if name else None
