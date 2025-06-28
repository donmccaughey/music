from pytest import fixture


from .command import CommandType
from .lines import Blank, Error
from .parse import parse_line, parse_lines
from .rem import Rem
from .title import Title


@fixture
def command_type_map() -> dict[str, CommandType]:
    return {
        'REM': Rem,
        'TITLE': Title,
    }


def test_parse_line_for_known_command(command_type_map):
    line_str = 'TITLE "Gimme Shelter"'
    line = parse_line(command_type_map, 42, line_str)

    assert line.line_number == 42
    assert line.line == line_str
    assert isinstance(line, Title)
    assert line.title == 'Gimme Shelter'


def test_parse_line_for_unknown_command(command_type_map):
    line_str = 'BARF "Unknown command"'
    line = parse_line(command_type_map, 42, line_str)

    assert line.line_number == 42
    assert line.line == line_str
    assert isinstance(line, Error)


def test_parse_lines(command_type_map):
    s = (
        'TITLE "Gimme Shelter"\n'
        'BARF "Unknown command"\n'
        '\n'
        'REM This is a reminder'
    )
    lines = parse_lines(command_type_map, s)
    assert lines == [
        Title(1, 'TITLE "Gimme Shelter"', 'Gimme Shelter'),
        Error(2, 'BARF "Unknown command"'),
        Blank(3, ''),
        Rem(4, 'REM This is a reminder', 'This is a reminder'),
    ]
