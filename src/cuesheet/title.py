from typing import Optional
from .parse import parse_quoted_string
from .statement import Statement


class Title(Statement):
    def __init__(self, line_number: int, line: str, title: str):
        super().__init__(line_number, line)
        self.title = title

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Title']:
        name = parse_quoted_string('TITLE', line)
        return Title(line_number, line, name) if name else None
