from typing import TextIO, Generator

from .commands import (
    CommandType,
    File,
    Index,
    Line,
    Performer,
    Rem,
    Title,
    Track,
)
from .commands.parse import parse_line


command_type_map: dict[str, CommandType] = {
    command_type.__name__.upper(): command_type
    for command_type in [
        File,
        Index,
        Performer,
        Rem,
        Title,
        Track,
    ]
}


class Lexer:
    def __init__(self, source: TextIO):
        self.source = source

    def commands(self) -> Generator[Line]:
        for i, line in enumerate(self.source):
            yield parse_line(command_type_map, i + 1, line.strip('\n'))
