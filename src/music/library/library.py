from __future__ import annotations

from pathlib import Path

from .album import Album
from .artist import Artist


class Library:
    def __init__(self, library_root: Path, artists: list[Artist]):
        self.library_root = library_root
        self.artists = artists
        self.artists_by_name = {artist.name: artist for artist in artists}

    def get_artist(self, name: str) -> Artist | None:
        return self.artists_by_name.get(name)

    def get_album(self, artist_name: str, album_title: str) -> Album | None:
        artist = self.get_artist(artist_name)
        return artist.get_album(album_title) if artist else None

    @classmethod
    def load(cls, library_root: Path) -> Library:
        artists = []

        for path in library_root.iterdir():
            if path.is_dir():
                rel_artist_dir = path.relative_to(library_root)
                artists.append(Artist.load(library_root, rel_artist_dir))

        return cls(library_root, artists)
