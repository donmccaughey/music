from dataclasses import dataclass
from typing import Optional, Type, TypeVar

from .lines import Line

F = TypeVar('F', bound='Field')


@dataclass
class Field(Line):
    @classmethod
    def parse(cls: Type[F], line_number: int, line: str) -> Optional[F]:
        raise NotImplementedError()
