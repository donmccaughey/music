from dataclasses import dataclass
from typing import Optional

from .field import Field
from .parse import parse_quoted_string


@dataclass
class Performer(Field):
    name: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Performer']:
        name = parse_quoted_string('PERFORMER', line)
        return Performer(line_number, line, name) if name else None
