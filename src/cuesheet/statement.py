from typing import Optional, Type, TypeVar

S = TypeVar('S', bound='Statement')


class Statement:
    def __init__(self, line_number: int, line: str):
        self.line_number = line_number
        self.line = line

    @classmethod
    def parse(cls: Type[S], line_number: int, line: str) -> Optional[S]:
        raise NotImplementedError()
