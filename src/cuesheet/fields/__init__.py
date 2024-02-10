from typing import Type
from typing import TypeVar

from .field import Field
from .file import File
from .index import Index
from .lines import Blank
from .lines import Error
from .lines import Line
from .parse import to_tokens
from .performer import Performer
from .title import Title
from .track import Track

F = TypeVar('F', bound=Field)

FieldType = Type[F]

field_types: list[FieldType] = [
    Index,
    Performer,
    Title,
]

field_type_map: dict[str, FieldType] = {
    field_type.__name__.upper(): field_type for field_type in field_types
}


def parse_lines(s: str) -> list[Line]:
    return [parse_line(i + 1, line) for (i, line) in enumerate(s.splitlines())]


def parse_line(line_number: int, line: str) -> Line:
    tokens = to_tokens(line)

    if not tokens:
        return Blank(line_number, line)

    type_name = tokens[0]
    if type_name in field_type_map:
        parser = field_type_map[type_name]
        statement = parser.parse(line_number, line)
        return statement if statement else Error(line_number, line)

    return Error(line_number, line)
