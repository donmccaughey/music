from dataclasses import dataclass
from typing import Optional

from .field import Field
from .parse import to_ints, to_tokens


@dataclass
class Index(Field):
    number: int
    minutes: int
    seconds: int
    frames: int

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Index']:
        tokens = to_tokens(line)
        if len(tokens) != 3:
            return None

        if tokens[0].upper() != 'INDEX':
            return None
        if tokens[1].isdigit():
            number = int(tokens[1])
        else:
            return None
        times = to_ints(tokens[2], ':')
        if len(times) != 3:
            return None

        minutes, seconds, frames = times
        # TODO: validate ranges
        return Index(line_number, line, number, minutes, seconds, frames)
