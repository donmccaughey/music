from dataclasses import dataclass
from typing import Self

from .lines import Line


@dataclass
class Command(Line):
    @classmethod
    def parse(cls, line_number: int, line: str) -> Self | None:
        raise NotImplementedError()
