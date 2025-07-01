from io import StringIO

from music.cuesheet.commands import Blank, Error, Line, Rem, Title

from .lexer import Lexer


def test_scan():
    s = (
        '  TITLE "Gimme Shelter"\n'
        'BARF "Unknown command"\n'
        '\n'
        'REM This is a reminder'
    )
    lexer = Lexer()
    commands = lexer.scan(StringIO(s))
    assert list(commands) == [
        Title(Line(1, '  TITLE "Gimme Shelter"'), 'Gimme Shelter'),
        Error(2, 'BARF "Unknown command"'),
        Blank(Line(3, '')),
        Rem(Line(4, 'REM This is a reminder'), 'This is a reminder'),
    ]


def test_scan_line_for_known_command():
    line_str = 'TITLE "Gimme Shelter"'
    lexer = Lexer()
    line = lexer.scan_line(42, line_str)

    assert line.line == Line(42, line_str)
    assert isinstance(line, Title)
    assert line.title == 'Gimme Shelter'


def test_scan_line_for_unknown_command():
    line_str = 'BARF "Unknown command"'
    lexer = Lexer()
    line = lexer.scan_line(42, line_str)

    assert line == Error(42, line_str)
