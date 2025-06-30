from typing import TextIO, Generator

from .commands import (
    Blank,
    CommandType,
    Error,
    File,
    Index,
    Line,
    Performer,
    Rem,
    split_tokens,
    Title,
    Track,
)


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


def parse_lines(command_type_map: dict[str, CommandType], s: str) -> list[Line]:
    return [
        parse_line(command_type_map, i + 1, line)
        for (i, line) in enumerate(s.splitlines())
    ]


def parse_line(
    command_type_map: dict[str, CommandType], line_number: int, line: str
) -> Line:
    tokens = split_tokens(line)

    if not tokens:
        return Blank(line_number, line)

    command_name = tokens[0]
    if command_name in command_type_map:
        command_type = command_type_map[command_name]
        command = command_type.parse(line_number, line)
        return command if command else Error(line_number, line)

    return Error(line_number, line)
