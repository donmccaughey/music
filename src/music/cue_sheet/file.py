from pathlib import Path

from .error import Error
from .track import Track


class File:
    def __init__(self, filename: Path, file_type: str):
        self.filename = filename
        self.type = file_type
        self.remarks: list[str] = []
        self.tracks: list[Track] = []
        self.errors: list[Error] = []
