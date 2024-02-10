from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .field import Field
from .parse import to_tokens
from .track import Track


@dataclass
class File(Field):
    filename: Path
    file_type: str
    tracks: list[Track]

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['File']:
        tokens = to_tokens(line)
        if len(tokens) != 3:
            # TODO: handle any filename, not just "album.wav"
            return None

        if tokens[0].upper() != 'FILE':
            return None
        if tokens[1].startswith('"') and tokens[1].endswith('"'):
            filename = tokens[1][1:-1]
        else:
            return None

        file_type = tokens[2]
        # TODO: is WAVE the only valid type?

        return File(line_number, line, Path(filename), file_type, [])
