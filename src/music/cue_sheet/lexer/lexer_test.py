from io import StringIO

import pytest

from music.cue_sheet import IndexPoint

from .lexer import Lexer
from .token import Token
from .token_type import TokenType


@pytest.mark.parametrize(
    'source, expected_tokens',
    [
        (
            (
                'FILE "album.wav" WAVE\n'
                '  TRACK 01 AUDIO\n'
                '    TITLE "Gimme Shelter"\n'
                '    PERFORMER "The Rolling Stones"\n'
                '    INDEX 01 04:32:38\n'
            ),
            [
                Token(1, TokenType.NAME, 'FILE'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.QSTR, 'album.wav'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.NAME, 'WAVE'),
                Token(1, TokenType.EOL, '\n'),
                #
                Token(2, TokenType.WS, '  '),
                Token(2, TokenType.NAME, 'TRACK'),
                Token(2, TokenType.WS, ' '),
                Token(2, TokenType.INT, 1),
                Token(2, TokenType.WS, ' '),
                Token(2, TokenType.NAME, 'AUDIO'),
                Token(2, TokenType.EOL, '\n'),
                #
                Token(3, TokenType.WS, '    '),
                Token(3, TokenType.NAME, 'TITLE'),
                Token(3, TokenType.WS, ' '),
                Token(3, TokenType.QSTR, 'Gimme Shelter'),
                Token(3, TokenType.EOL, '\n'),
                #
                Token(4, TokenType.WS, '    '),
                Token(4, TokenType.NAME, 'PERFORMER'),
                Token(4, TokenType.WS, ' '),
                Token(4, TokenType.QSTR, 'The Rolling Stones'),
                Token(4, TokenType.EOL, '\n'),
                #
                Token(5, TokenType.WS, '    '),
                Token(5, TokenType.NAME, 'INDEX'),
                Token(5, TokenType.WS, ' '),
                Token(5, TokenType.INT, 1),
                Token(5, TokenType.WS, ' '),
                Token(5, TokenType.IDX_PT, IndexPoint(4, 32, 38)),
                Token(5, TokenType.EOL, '\n'),
            ],
        ),
    ],
)
def test_lex(source, expected_tokens):
    lexer = Lexer(StringIO(source))
    tokens = list(lexer.lex())

    assert tokens == expected_tokens


@pytest.mark.parametrize(
    'line, expected_tokens',
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
            'FILE "album.wav" \n',
            [
                Token(1, TokenType.NAME, 'FILE'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.QSTR, 'album.wav'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.EOL, '\n'),
            ],
        ),
        (
            'INDEX 01 04:32:38',
            [
                Token(1, TokenType.NAME, 'INDEX'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.INT, 1),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.IDX_PT, IndexPoint(4, 32, 38)),
            ],
        ),
        (
            'INDEX 01 04:32',
            [
                Token(1, TokenType.NAME, 'INDEX'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.INT, 1),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.STR, '04:32'),
            ],
        ),
        (
            'PERFORMER "Alice and Bob"',
            [
                Token(1, TokenType.NAME, 'PERFORMER'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.QSTR, 'Alice and Bob'),
            ],
        ),
        (
            'REM An unquoted comment\n',
            [
                Token(1, TokenType.NAME, 'REM'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.STR, 'An'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.STR, 'unquoted'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.STR, 'comment'),
                Token(1, TokenType.EOL, '\n'),
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
        (
            'TITLE "No closing quote',
            [
                Token(1, TokenType.NAME, 'TITLE'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.STR, '"No closing quote'),
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
            'TRACK 11',
            [
                Token(1, TokenType.NAME, 'TRACK'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.INT, 11),
            ],
        ),
    ],
)
def test_lex_line(line, expected_tokens):
    lexer = Lexer(StringIO(line))
    tokens = list(lexer._lex_line(1, line))

    assert tokens == expected_tokens
