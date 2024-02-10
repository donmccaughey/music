from typing import Optional

from .statement import Statement


class Blank(Statement):
    def __init__(self, line_number: int, line: str):
        super().__init__(line_number, line)

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Blank']:
        if line.strip():
            return None
        else:
            return cls(line_number, line)
