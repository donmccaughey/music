from io import StringIO

import pytest

from music.cue_sheet import IndexPoint

from .lexer import Lexer
from .token import Token
from .token_type import EOL, IDX_PT, INT, NAME, QSTR, STR, WS


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
                Token(1, NAME, 'FILE'),
                Token(1, WS, ' '),
                Token(1, QSTR, 'album.wav'),
                Token(1, WS, ' '),
                Token(1, NAME, 'WAVE'),
                Token(1, EOL, '\n'),
                #
                Token(2, WS, '  '),
                Token(2, NAME, 'TRACK'),
                Token(2, WS, ' '),
                Token(2, INT, 1),
                Token(2, WS, ' '),
                Token(2, NAME, 'AUDIO'),
                Token(2, EOL, '\n'),
                #
                Token(3, WS, '    '),
                Token(3, NAME, 'TITLE'),
                Token(3, WS, ' '),
                Token(3, QSTR, 'Gimme Shelter'),
                Token(3, EOL, '\n'),
                #
                Token(4, WS, '    '),
                Token(4, NAME, 'PERFORMER'),
                Token(4, WS, ' '),
                Token(4, QSTR, 'The Rolling Stones'),
                Token(4, EOL, '\n'),
                #
                Token(5, WS, '    '),
                Token(5, NAME, 'INDEX'),
                Token(5, WS, ' '),
                Token(5, INT, 1),
                Token(5, WS, ' '),
                Token(5, IDX_PT, IndexPoint(4, 32, 38)),
                Token(5, EOL, '\n'),
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
                Token(1, NAME, 'FILE'),
                Token(1, WS, ' '),
                Token(1, QSTR, 'album.wav'),
                Token(1, WS, ' '),
                Token(1, NAME, 'WAVE'),
                Token(1, EOL, '\n'),
            ],
        ),
        (
            'FILE "album.wav" \n',
            [
                Token(1, NAME, 'FILE'),
                Token(1, WS, ' '),
                Token(1, QSTR, 'album.wav'),
                Token(1, WS, ' '),
                Token(1, EOL, '\n'),
            ],
        ),
        (
            'INDEX 01 04:32:38',
            [
                Token(1, NAME, 'INDEX'),
                Token(1, WS, ' '),
                Token(1, INT, 1),
                Token(1, WS, ' '),
                Token(1, IDX_PT, IndexPoint(4, 32, 38)),
            ],
        ),
        (
            'INDEX 01 04:32',
            [
                Token(1, NAME, 'INDEX'),
                Token(1, WS, ' '),
                Token(1, INT, 1),
                Token(1, WS, ' '),
                Token(1, STR, '04:32'),
            ],
        ),
        (
            'PERFORMER "Alice and Bob"',
            [
                Token(1, NAME, 'PERFORMER'),
                Token(1, WS, ' '),
                Token(1, QSTR, 'Alice and Bob'),
            ],
        ),
        (
            'REM An unquoted comment\n',
            [
                Token(1, NAME, 'REM'),
                Token(1, WS, ' '),
                Token(1, STR, 'An'),
                Token(1, WS, ' '),
                Token(1, STR, 'unquoted'),
                Token(1, WS, ' '),
                Token(1, STR, 'comment'),
                Token(1, EOL, '\n'),
            ],
        ),
        (
            'TITLE "Gimme Shelter"\n',
            [
                Token(1, NAME, 'TITLE'),
                Token(1, WS, ' '),
                Token(1, QSTR, 'Gimme Shelter'),
                Token(1, EOL, '\n'),
            ],
        ),
        (
            'TITLE "No closing quote',
            [
                Token(1, NAME, 'TITLE'),
                Token(1, WS, ' '),
                Token(1, STR, '"No closing quote'),
            ],
        ),
        (
            '  TRACK  01  AUDIO  ',
            [
                Token(1, WS, '  '),
                Token(1, NAME, 'TRACK'),
                Token(1, WS, '  '),
                Token(1, INT, 1),
                Token(1, WS, '  '),
                Token(1, NAME, 'AUDIO'),
                Token(1, WS, '  '),
            ],
        ),
        (
            'TRACK 11',
            [
                Token(1, NAME, 'TRACK'),
                Token(1, WS, ' '),
                Token(1, INT, 11),
            ],
        ),
    ],
)
def test_lex_line(line, expected_tokens):
    lexer = Lexer(StringIO(line))
    tokens = list(lexer._lex_line(1, line))

    assert tokens == expected_tokens
