from dataclasses import dataclass
from .file import File


@dataclass
class Cuesheet:
    performer: str
    title: str
    year: int
    genre: str
    asin: str
    discid: str
    comment: str
    file: File
