from dataclasses import dataclass
from typing import Type, TypeVar

from .lines import Line

C = TypeVar('C', bound='Command')
CommandType = Type[C]


@dataclass
class Command(Line):
    @classmethod
    def parse(cls: Type[C], line_number: int, line: str) -> C | None:
        raise NotImplementedError()
