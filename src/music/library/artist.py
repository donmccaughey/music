from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .album import Album


@dataclass
class Artist:
    library_root: Path
    rel_artist_dir: Path
    name: str
    albums: list[Album]

    @classmethod
    def load(cls, library_root: Path, rel_artist_dir: Path) -> Artist:
        name = rel_artist_dir.name
        albums = []

        artist_dir = library_root / rel_artist_dir
        for path in artist_dir.iterdir():
            if path.is_dir():
                rel_album_dir = path.relative_to(library_root)
                albums.append(Album.load(library_root, rel_album_dir))

        return Artist(
            library_root=library_root,
            rel_artist_dir=rel_artist_dir,
            name=name,
            albums=albums,
        )
