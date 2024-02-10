from typing import Optional
from .parse import parse_quoted_string
from .statement import Statement


class Performer(Statement):
    def __init__(self, line_number: int, line: str, name: str):
        super().__init__(line_number, line)
        self.name = name

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Performer']:
        name = parse_quoted_string('PERFORMER', line)
        return Performer(line_number, line, name) if name else None
