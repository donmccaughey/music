from pathlib import Path

from .album import Album
from .artist import Artist


class Library:
    def __init__(self, folder: Path, paths: list[Path]):
        self.folder = folder
        self.artists: list[Artist] = []
        self.artists_by_name: dict[str, Artist] = {}

        for path in paths:
            relative_path = path.relative_to(self.folder)
            artist_folder = relative_path.parent
            artist_name, album_title, _ = relative_path.parts

            if not self.artists or artist_name != self.artists[-1].name:
                artist = Artist(
                    folder=artist_folder, name=artist_name, albums=[]
                )
                self.artists.append(artist)
                self.artists_by_name[artist_name] = artist

            album = Album(folder=relative_path, title=album_title)
            self.artists[-1].albums.append(album)

        self.artists.sort(key=lambda a: a.name)
