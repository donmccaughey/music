from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .track import Track


@dataclass
class Album:
    library_root: Path
    rel_album_dir: Path
    title: str
    covers: list[Path]
    cue_sheets: list[Path]
    flac_files: list[Path]
    tracks: list[Track]

    @classmethod
    def load(cls, library_root: Path, rel_album_dir: Path) -> Album:
        title = rel_album_dir.name
        covers = []
        cue_sheets = []
        flac_files = []
        tracks = []

        album_dir = library_root / rel_album_dir
        for path in album_dir.iterdir():
            if path.is_file():
                if is_cover(path):
                    covers.append(path)
                elif is_cuesheet(path):
                    cue_sheets.append(path)
                elif is_flac(path):
                    flac_files.append(path)
                elif is_track(path):
                    rel_track_dir = path.relative_to(library_root)
                    track = Track.load(library_root, rel_track_dir)
                    tracks.append(track)

        return cls(
            library_root=library_root,
            rel_album_dir=rel_album_dir,
            title=title,
            covers=covers,
            cue_sheets=cue_sheets,
            flac_files=flac_files,
            tracks=tracks,
        )


def is_cover(path: Path) -> bool:
    return 'cover.jpg' == path.name


def is_cuesheet(path: Path) -> bool:
    return path.name in [
        'cuesheet.txt',
        'cuesheet1.txt',
        'cuesheet2.txt',
        'cuesheet3.txt',
    ]


def is_flac(path: Path) -> bool:
    return '.flac' == path.suffix


def is_track(path: Path) -> bool:
    return path.suffix in ['.mp3', '.m4a']
