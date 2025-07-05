import pytest

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .file import File
from .parser import Parser
from .performer import Performer
from .root import Root
from .title import Title
from .track import Track


@pytest.mark.parametrize(
    'tokens, expected',
    [
        (
            [
                Token(1, TokenType.NAME, 'PERFORMER'),
                Token(1, TokenType.WS, ' '),
                Token(1, TokenType.QSTR, 'The Rolling Stones'),
                Token(1, TokenType.EOL, '\n'),
                Token(2, TokenType.NAME, 'TITLE'),
                Token(2, TokenType.WS, ' '),
                Token(2, TokenType.QSTR, 'Gimme Shelter'),
                Token(2, TokenType.EOL, '\n'),
                Token(3, TokenType.NAME, 'FILE'),
                Token(3, TokenType.WS, ' '),
                Token(3, TokenType.QSTR, 'album.wav'),
                Token(3, TokenType.WS, ' '),
                Token(3, TokenType.NAME, 'WAVE'),
                Token(3, TokenType.EOL, '\n'),
                Token(4, TokenType.NAME, 'TRACK'),
                Token(4, TokenType.WS, ' '),
                Token(4, TokenType.INT, 1),
                Token(4, TokenType.WS, ' '),
                Token(4, TokenType.NAME, 'AUDIO'),
                Token(4, TokenType.EOL, '\n'),
                Token(8, TokenType.NAME, 'TRACK'),
                Token(8, TokenType.WS, ' '),
                Token(8, TokenType.INT, 2),
                Token(8, TokenType.WS, ' '),
                Token(8, TokenType.NAME, 'AUDIO'),
                Token(8, TokenType.EOL, '\n'),
            ],
            Root(
                [
                    Performer(
                        [
                            Token(1, TokenType.NAME, 'PERFORMER'),
                            Token(1, TokenType.QSTR, 'The Rolling Stones'),
                            Token(1, TokenType.EOL, '\n'),
                        ],
                    ),
                    Title(
                        [
                            Token(2, TokenType.NAME, 'TITLE'),
                            Token(2, TokenType.QSTR, 'Gimme Shelter'),
                            Token(2, TokenType.EOL, '\n'),
                        ]
                    ),
                    File(
                        tokens=[
                            Token(3, TokenType.NAME, 'FILE'),
                            Token(3, TokenType.QSTR, 'album.wav'),
                            Token(3, TokenType.NAME, 'WAVE'),
                            Token(3, TokenType.EOL, '\n'),
                        ],
                        children=[
                            Track(
                                tokens=[
                                    Token(4, TokenType.NAME, 'TRACK'),
                                    Token(4, TokenType.INT, 1),
                                    Token(4, TokenType.NAME, 'AUDIO'),
                                    Token(4, TokenType.EOL, '\n'),
                                ],
                                children=[],
                            ),
                            Track(
                                tokens=[
                                    Token(8, TokenType.NAME, 'TRACK'),
                                    Token(8, TokenType.INT, 2),
                                    Token(8, TokenType.NAME, 'AUDIO'),
                                    Token(8, TokenType.EOL, '\n'),
                                ],
                                children=[],
                            ),
                        ],
                    ),
                ]
            ),
        ),
    ],
)
def test_parser(tokens, expected):
    parser = Parser(iter(tokens))

    assert parser.parse() == expected
