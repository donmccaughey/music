from .error import Error
from .file import File


class CueSheet:
    def __init__(self):
        self.performer: str | None = None
        self.title: str | None = None
        self.year: int | None = None
        self.genre: str | None = None
        self.asin: str | None = None
        self.disc_id: str | None = None
        self.comment: str | None = None
        self.remarks: list[str] = []
        self.file: File | None = None
        self.errors: list[Error] = []
