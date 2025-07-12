from .index_point import IndexPoint


class Track:
    def __init__(self, number: int, track_type: str):
        self.number = number
        self.type = track_type
        self.title: str | None = None
        self.performer: str | None = None
        self.indices: dict[int, IndexPoint] = {}
        self.remarks: list[str] = []
