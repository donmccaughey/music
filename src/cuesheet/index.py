from dataclasses import dataclass
from typing import Union

@dataclass
class Index:
    number: int
    minutes: int
    seconds: int
    frames: int

    @staticmethod
    def parse(index_string: str) -> Union['Index', None]:
        tokens = to_tokens(index_string)
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
        return Index(number, minutes, seconds, frames)


def to_ints(s: str, separator: str) -> list[int]:
    return [int(token) for token in s.split(separator) if token.isdigit()]


def to_tokens(s: str) -> list[str]:
    return [token for token in s.split() if token]
