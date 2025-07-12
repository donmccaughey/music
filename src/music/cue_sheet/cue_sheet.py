from __future__ import annotations

from collections import namedtuple
from pathlib import Path

from .index_point import IndexPoint


Error2 = namedtuple('Error2', ('line_num', 'value'))


class Track2:
    def __init__(self, number: int, track_type: str):
        self.number = number
        self.type = track_type
        self.title: str | None = None
        self.performer: str | None = None
        self.indices: dict[int, IndexPoint] = {}
        self.remarks: list[str] = []


class File2:
    def __init__(self, filename: Path, file_type: str):
        self.filename = filename
        self.type = file_type
        self.remarks: list[str] = []
        self.tracks: list[Track2] = []
        self.errors: list[Error2] = []


class CueSheet2:
    def __init__(self):
        self.performer: str | None = None
        self.title: str | None = None
        self.year: int | None = None
        self.genre: str | None = None
        self.asin: str | None = None
        self.disc_id: str | None = None
        self.comment: str | None = None
        self.remarks: list[str] = []
        self.file: File2 | None = None
        self.errors: list[Error2] = []
