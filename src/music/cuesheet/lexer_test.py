from io import StringIO

from .commands import Blank, Error, Rem, Title
from .lexer import Lexer


def test_commands():
    s = (
        '  TITLE "Gimme Shelter"\n'
        'BARF "Unknown command"\n'
        '\n'
        'REM This is a reminder'
    )
    lexer = Lexer(StringIO(s))
    commands = lexer.commands()
    assert list(commands) == [
        Title(1, '  TITLE "Gimme Shelter"', 'Gimme Shelter'),
        Error(2, 'BARF "Unknown command"'),
        Blank(3, ''),
        Rem(4, 'REM This is a reminder', 'This is a reminder'),
    ]
