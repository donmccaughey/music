from dataclasses import dataclass
from pathlib import Path

from .track import Track


@dataclass
class File:
    filename: Path
    type: str
    tracks: list[Track]
