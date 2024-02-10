from .lines import Blank
from .lines import Error
from .lines import Line
from .split import split_tokens
from .type_map import type_map


def parse_lines(s: str) -> list[Line]:
    return [parse_line(i + 1, line) for (i, line) in enumerate(s.splitlines())]


def parse_line(line_number: int, line: str) -> Line:
    tokens = split_tokens(line)

    if not tokens:
        return Blank(line_number, line)

    type_name = tokens[0]
    if type_name in type_map:
        parser = type_map[type_name]
        statement = parser.parse(line_number, line)
        return statement if statement else Error(line_number, line)

    return Error(line_number, line)
