from dataclasses import dataclass
from pathlib import Path


@dataclass
class Album:
    folder: Path
    title: str
