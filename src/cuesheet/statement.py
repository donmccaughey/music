from dataclasses import dataclass
from typing import Optional, Type, TypeVar

S = TypeVar('S', bound='Statement')


@dataclass
class Statement:
    line_number: int
    line: str

    @classmethod
    def parse(cls: Type[S], line_number: int, line: str) -> Optional[S]:
        raise NotImplementedError()
