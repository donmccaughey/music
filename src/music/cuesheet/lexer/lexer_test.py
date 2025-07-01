from io import StringIO

import pytest

from music.cuesheet.commands import Blank, Error, Rem, Title

from .lexer import Lexer
from .line import Line
from .token import Token
from .token_type import TokenType


@pytest.mark.parametrize(
    'source, expected_tokens',
    [
        (
            'FILE "album.wav" WAVE\n',
            [
                Token(1, TokenType.NAME, 'FILE'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.QSTR, 'album.wav'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.NAME, 'WAVE'),
                Token(1, TokenType.EOL, '\n'),
            ],
        ),
        (
            '  TRACK  01  AUDIO  ',
            [
                Token(1, TokenType.WS, '  '),
                Token(1, TokenType.NAME, 'TRACK'),
                Token(1, TokenType.WS, '  '),
                Token(1, TokenType.INT, 1),
                Token(1, TokenType.WS, '  '),
                Token(1, TokenType.NAME, 'AUDIO'),
                Token(1, TokenType.WS, '  '),
            ],
        ),
        (
            'TITLE "Gimme Shelter"\n',
            [
                Token(1, TokenType.NAME, 'TITLE'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.QSTR, 'Gimme Shelter'),
                Token(1, TokenType.EOL, '\n'),
            ],
        ),
    ],
)
def test_lex(source, expected_tokens):
    lexer = Lexer()
    tokens = list(lexer.lex(StringIO(source)))

    assert tokens == expected_tokens


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
        Error(Line(2, 'BARF "Unknown command"')),
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

    assert line == Error(Line(42, line_str))
