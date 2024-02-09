from dataclasses import dataclass
from typing import Optional
from .parse import parse_quoted_string


@dataclass
class Title:
    title: str

    @staticmethod
    def parse(statement: str) -> Optional['Title']:
        title = parse_quoted_string('TITLE', statement)
        return Title(title) if title else None
