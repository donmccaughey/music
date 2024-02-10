from .fields import Blank
from .fields import Error
from .fields import File
from .fields import Index
from .fields import Line
from .fields import Performer
from .fields import Title
from .fields import parse_lines


class CueSheet:
    def __init__(self):
        self.lines: list[Line] = []
        self.performer: Performer | None = None
        self.title: Title | None = None
        self.year: int | None = None
        self.genre: str | None = None
        self.asin: str | None = None
        self.discid: str | None = None
        self.comment: str | None = None
        self.file: File | None = None

    @property
    def errors(self) -> list[Error]:
        return [line for line in self.lines if isinstance(line, Error)]

    @staticmethod
    def parse(s: str) -> 'CueSheet':
        cue_sheet = CueSheet()
        cue_sheet.lines = parse_lines(s)
        for line in cue_sheet.lines:
            match line:
                case Blank():
                    pass
                case Error():
                    pass
                case File():
                    cue_sheet.file = line
                case Index():
                    pass
                case Performer():
                    cue_sheet.performer = line
                case Title():
                    cue_sheet.title = line
                case _:
                    raise RuntimeError(f'Unsupported line type {line}')
        return cue_sheet
