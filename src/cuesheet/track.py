from dataclasses import dataclass
from .index import Index


@dataclass
class Track:
    number: int
    type: str
    title: str
    performer: str
    indices: list[Index]
