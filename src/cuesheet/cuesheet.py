from typing import Type, TypeVar

from .blank import Blank
from .error import Error
from .file import File
from .index import Index
from .line import Line
from .parse import to_tokens
from .performer import Performer
from .field import Field
from .title import Title


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
                case Index():
                    pass
                case Performer():
                    cue_sheet.performer = line
                case Title():
                    cue_sheet.title = line
                case _:
                    raise RuntimeError(f'Unsupported line type {line}')
        return cue_sheet


def parse_lines(s: str) -> list[Line]:
    return [parse_line(i + 1, line) for (i, line) in enumerate(s.splitlines())]


P = TypeVar('P', bound=Field)
Parser = Type[P]
parsers: list[Parser] = [
    Index,
    Performer,
    Title,
]
parser_map: dict[str, Parser] = {
    parser.__name__.upper(): parser for parser in parsers
}


def parse_line(line_number: int, line: str) -> Line:
    tokens = to_tokens(line)

    if not tokens:
        return Blank(line_number, line)

    type_name = tokens[0]
    if type_name in parser_map:
        parser = parser_map[type_name]
        statement = parser.parse(line_number, line)
        return statement if statement else Error(line_number, line)

    return Error(line_number, line)
