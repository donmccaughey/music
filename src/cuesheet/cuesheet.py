from .commands import Blank
from .commands import Error
from .commands import File
from .commands import Index
from .commands import Performer
from .commands import Title
from .commands import Track
from .commands import parse_lines


class CueSheet:
    def __init__(self):
        self.performer: Performer | None = None
        self.title: Title | None = None
        self.year: int | None = None
        self.genre: str | None = None
        self.asin: str | None = None
        self.discid: str | None = None
        self.comment: str | None = None
        self.file: File | None = None
        self.errors: list[Error] = []

    @staticmethod
    def parse(s: str) -> 'CueSheet':
        cue_sheet = CueSheet()
        for line in parse_lines(s):
            match line:
                case Blank():
                    pass
                case Error():
                    pass
                case File() as file:
                    cue_sheet.file = file
                case Index() as index:
                    if cue_sheet.file:
                        cue_sheet.file.tracks[-1].indices.append(index)
                    else:
                        cue_sheet.errors.append(Error.from_line(index))
                case Performer() as performer:
                    if not cue_sheet.performer:
                        cue_sheet.performer = performer
                    elif cue_sheet.file and cue_sheet.file.tracks:
                        cue_sheet.file.tracks[-1].performer = performer
                    else:
                        cue_sheet.errors.append(Error.from_line(performer))
                case Title() as title:
                    if not cue_sheet.title:
                        cue_sheet.title = title
                    elif not cue_sheet.file or not cue_sheet.file.tracks:
                        cue_sheet.errors.append(Error.from_line(title))
                    else:
                        cue_sheet.file.tracks[-1].title = title
                case Track() as track:
                    if cue_sheet.file:
                        cue_sheet.file.tracks.append(track)
                    else:
                        cue_sheet.errors.append(Error.from_line(track))
                case _:
                    raise RuntimeError(f'Unsupported line type {line}')
        return cue_sheet
