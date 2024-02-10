from dataclasses import dataclass
from typing import Optional
from .parse import parse_quoted_string
from .statement import Statement


@dataclass
class Title(Statement):
    title: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Title']:
        name = parse_quoted_string('TITLE', line)
        return Title(line_number, line, name) if name else None
