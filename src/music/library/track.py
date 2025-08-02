from __future__ import annotations

import re

from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path


Filename = namedtuple('Filename', ('number', 'title', 'file_type'))


@dataclass
class Track:
    library_root: Path
    rel_track_path: Path
    number: int
    title: str
    file_type: str

    @classmethod
    def load(cls, library_root: Path, rel_track_path: Path) -> Track:
        track_filename = parse_filename(rel_track_path)

        return cls(
            library_root=library_root,
            rel_track_path=rel_track_path,
            number=track_filename.number,
            title=track_filename.title,
            file_type=track_filename.file_type,
        )


NUMBERED_TRACK = re.compile(r'^(\d{2,3})\s(.*)')


def parse_filename(filename: Path) -> Filename:
    if match := NUMBERED_TRACK.match(filename.stem):
        number = int(match.group(1))
        title = match.group(2)
    else:
        number = 0
        title = filename.stem
    file_type = filename.suffix[1:]
    return Filename(number, title, file_type)
