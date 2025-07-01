from __future__ import annotations

from io import StringIO

from .commands import Blank
from .commands import Error
from .commands import File
from .commands import Index
from .commands import Performer
from .commands import Rem
from .commands import Title
from .commands import Track
from .lexer import Lexer


class CueSheet:
    def __init__(self):
        self.performer: Performer | None = None
        self.title: Title | None = None
        self.year: int | None = None
        self.genre: str | None = None
        self.asin: str | None = None
        self.discid: str | None = None
        self.comment: str | None = None
        self.remarks: list[Rem] = []
        self.file: File | None = None
        self.errors: list[Error] = []

    @classmethod
    def parse(cls, s: str) -> CueSheet:
        cue_sheet = cls()
        lexer = Lexer()
        for line in lexer.scan(StringIO(s)):
            match line:
                case Blank() as blank:
                    cue_sheet.parse_blank(blank)
                case Error() as error:
                    cue_sheet.parse_error(error)
                case File() as file:
                    cue_sheet.parse_file(file)
                case Index() as index:
                    cue_sheet.parse_index(index)
                case Performer() as performer:
                    cue_sheet.parse_performer(performer)
                case Rem() as rem:
                    cue_sheet.parse_rem(rem)
                case Title() as title:
                    cue_sheet.parse_title(title)
                case Track() as track:
                    cue_sheet.parse_track(track)
                case _:
                    raise RuntimeError(f'Unsupported line type {line}')
        return cue_sheet

    def parse_blank(self, blank: Blank):
        pass

    def parse_error(self, error: Error):
        self.errors.append(error)

    def parse_file(self, file: File):
        self.file = file

    def parse_index(self, index: Index):
        if self.file and self.file.tracks:
            self.file.tracks[-1].indices.append(index)
        else:
            self.errors.append(Error(index.line.line_number, index.line.line))

    def parse_performer(self, performer: Performer):
        if not self.performer:
            self.performer = performer
        elif self.file and self.file.tracks:
            self.file.tracks[-1].performer = performer
        else:
            self.errors.append(
                Error(performer.line.line_number, performer.line.line)
            )

    def parse_rem(self, rem: Rem):
        if self.file:
            if self.file.tracks:
                self.file.tracks[-1].remarks.append(rem)
            else:
                self.file.remarks.append(rem)
        else:
            self.remarks.append(rem)

    def parse_title(self, title: Title):
        if not self.title:
            self.title = title
        elif not self.file or not self.file.tracks:
            self.errors.append(Error(title.line.line_number, title.line.line))
        else:
            self.file.tracks[-1].title = title

    def parse_track(self, track: Track):
        if self.file:
            self.file.tracks.append(track)
        else:
            self.errors.append(Error(track.line.line_number, track.line.line))
