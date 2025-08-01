from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Track:
    library_root: Path
    rel_track_path: Path
    title: str

    @classmethod
    def load(cls, library_root: Path, rel_track_path: Path) -> Track:
        title = rel_track_path.name

        return cls(
            library_root=library_root,
            rel_track_path=rel_track_path,
            title=title,
        )
