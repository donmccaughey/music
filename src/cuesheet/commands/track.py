from dataclasses import dataclass
from typing import Optional

from .command import Command
from .index import Index
from .performer import Performer
from .rem import Rem
from .split import split_tokens
from .title import Title


@dataclass
class Track(Command):
    number: int
    track_type: str
    title: Title | None
    performer: Performer | None
    indices: list[Index]
    remarks: list[Rem]

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Track']:
        tokens = split_tokens(line)
        if len(tokens) != 3:
            return None

        if tokens[0].upper() != 'TRACK':
            return None

        if tokens[1].isdigit():
            number = int(tokens[1])
        else:
            return None

        track_type = tokens[2]

        return Track(line_number, line, number, track_type, None, None, [], [])
