from __future__ import annotations

from pathlib import Path

from .album import Album


class Artist:
    def __init__(
        self,
        library_root: Path,
        rel_artist_dir: Path,
        name: str,
        albums: list[Album],
    ):
        self.library_root = library_root
        self.rel_artist_dir = rel_artist_dir
        self.name = name
        self.albums = albums
        self.albums_by_title = {album.title: album for album in albums}

    def get_album(self, title: str) -> Album | None:
        return self.albums_by_title.get(title)

    @classmethod
    def load(cls, library_root: Path, rel_artist_dir: Path) -> Artist:
        name = rel_artist_dir.name
        albums = []

        artist_dir = library_root / rel_artist_dir
        for path in artist_dir.iterdir():
            if path.is_dir():
                rel_album_dir = path.relative_to(library_root)
                albums.append(Album.load(library_root, rel_album_dir))

        return cls(
            library_root=library_root,
            rel_artist_dir=rel_artist_dir,
            name=name,
            albums=albums,
        )
