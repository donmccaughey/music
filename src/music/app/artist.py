from dataclasses import dataclass
from pathlib import Path

from .album import Album


@dataclass
class Artist:
    folder: Path
    name: str
    albums: list[Album]
