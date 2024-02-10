from dataclasses import dataclass
from typing import Optional, Type, TypeVar

from .line import Line

S = TypeVar('S', bound='Statement')


@dataclass
class Statement(Line):
    @classmethod
    def parse(cls: Type[S], line_number: int, line: str) -> Optional[S]:
        raise NotImplementedError()
