from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .command import Command
from .rem import Rem
from .split import split_tokens
from .track import Track


@dataclass
class File(Command):
    filename: Path
    file_type: str | None
    remarks: list[Rem]
    tracks: list[Track]

    @classmethod
    def parse(cls, line_number: int, line: str) -> File | None:
        tokens = split_tokens(line)
        if len(tokens) not in (2, 3):
            # TODO: handle any filename, not just "album.wav"
            return None

        if tokens[0].upper() != 'FILE':
            return None

        if tokens[1].startswith('"') and tokens[1].endswith('"'):
            filename = tokens[1][1:-1]
        else:
            return None

        file_type = tokens[2] if len(tokens) > 2 else None
        # TODO: is WAVE the only valid type?

        return cls(line_number, line, Path(filename), file_type, [], [])
