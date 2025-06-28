from .command import CommandType
from .lines import Blank
from .lines import Error
from .lines import Line
from .split import split_tokens


def parse_lines(command_type_map: dict[str, CommandType], s: str) -> list[Line]:
    return [parse_line(command_type_map, i + 1, line) for (i, line) in enumerate(s.splitlines())]


def parse_line(command_type_map: dict[str, CommandType], line_number: int, line: str) -> Line:
    tokens = split_tokens(line)

    if not tokens:
        return Blank(line_number, line)

    command_name = tokens[0]
    if command_name in command_type_map:
        command_type = command_type_map[command_name]
        command = command_type.parse(line_number, line)
        return command if command else Error(line_number, line)

    return Error(line_number, line)
