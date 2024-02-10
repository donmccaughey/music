from dataclasses import dataclass
from typing import Optional

from .statement import Statement


@dataclass
class Blank(Statement):
    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Blank']:
        if line.strip():
            return None
        else:
            return cls(line_number, line)
