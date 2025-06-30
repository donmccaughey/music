from io import StringIO

from pytest import fixture

from .commands import Blank, CommandType, Error, Rem, Title
from .lexer import Lexer


def test_scan():
    s = (
        '  TITLE "Gimme Shelter"\n'
        'BARF "Unknown command"\n'
        '\n'
        'REM This is a reminder'
    )
    lexer = Lexer(StringIO(s))
    commands = lexer.scan()
    assert list(commands) == [
        Title(1, '  TITLE "Gimme Shelter"', 'Gimme Shelter'),
        Error(2, 'BARF "Unknown command"'),
        Blank(3, ''),
        Rem(4, 'REM This is a reminder', 'This is a reminder'),
    ]


@fixture
def command_type_map() -> dict[str, CommandType]:
    return {
        'REM': Rem,
        'TITLE': Title,
    }


def test_scan_line_for_known_command(command_type_map):
    line_str = 'TITLE "Gimme Shelter"'
    lexer = Lexer(StringIO(line_str))
    line = lexer.scan_line(command_type_map, 42, line_str)

    assert line.line_number == 42
    assert line.line == line_str
    assert isinstance(line, Title)
    assert line.title == 'Gimme Shelter'


def test_scan_line_for_unknown_command(command_type_map):
    line_str = 'BARF "Unknown command"'
    lexer = Lexer(StringIO(line_str))
    line = lexer.scan_line(command_type_map, 42, line_str)

    assert line.line_number == 42
    assert line.line == line_str
    assert isinstance(line, Error)
