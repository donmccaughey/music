from dataclasses import dataclass
from typing import Optional
from .parse import parse_quoted_string

@dataclass
class Performer:
    name: str

    @staticmethod
    def parse(statement: str) -> Optional['Performer']:
        name = parse_quoted_string('PERFORMER', statement)
        return Performer(name) if name else None
