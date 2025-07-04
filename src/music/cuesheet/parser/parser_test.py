from music.cuesheet import IndexPoint
from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .file import File
from .index import Index
from .parser import Parser
from .performer import Performer
from .rem import Rem
from .root import Root
from .title import Title
from .track import Track
from .year import Year


def test_parser_for_normal_file():
    tokens = [
        Token(1, TokenType.NAME, 'PERFORMER'),
        Token(1, TokenType.WS, ' '),
        Token(1, TokenType.QSTR, 'The Rolling Stones'),
        Token(1, TokenType.EOL, '\n'),
        #
        Token(2, TokenType.NAME, 'TITLE'),
        Token(2, TokenType.WS, ' '),
        Token(2, TokenType.QSTR, 'Let It Bleed'),
        Token(2, TokenType.EOL, '\n'),
        #
        Token(3, TokenType.NAME, 'REM'),
        Token(3, TokenType.WS, ' '),
        Token(3, TokenType.NAME, 'YEAR'),
        Token(3, TokenType.WS, ' '),
        Token(3, TokenType.INT, 1969),
        Token(3, TokenType.EOL, '\n'),
        #
        Token(4, TokenType.NAME, 'REM'),
        Token(4, TokenType.WS, ' '),
        Token(4, TokenType.NAME, 'GENRE'),
        Token(4, TokenType.WS, ' '),
        Token(4, TokenType.QSTR, 'Classic Rock'),
        Token(4, TokenType.EOL, '\n'),
        #
        Token(5, TokenType.WS, ' '),
        Token(5, TokenType.EOL, '\n'),
        #
        Token(6, TokenType.NAME, 'FILE'),
        Token(6, TokenType.WS, ' '),
        Token(6, TokenType.QSTR, 'album.wav'),
        Token(6, TokenType.WS, ' '),
        Token(6, TokenType.NAME, 'WAVE'),
        Token(6, TokenType.EOL, '\n'),
        #
        Token(7, TokenType.WS, '  '),
        Token(7, TokenType.NAME, 'TRACK'),
        Token(7, TokenType.WS, ' '),
        Token(7, TokenType.INT, 1),
        Token(7, TokenType.WS, ' '),
        Token(7, TokenType.NAME, 'AUDIO'),
        Token(7, TokenType.EOL, '\n'),
        #
        Token(8, TokenType.WS, '    '),
        Token(8, TokenType.NAME, 'TITLE'),
        Token(8, TokenType.WS, ' '),
        Token(8, TokenType.QSTR, 'Gimme Shelter'),
        Token(8, TokenType.EOL, '\n'),
        #
        Token(9, TokenType.WS, '    '),
        Token(9, TokenType.NAME, 'PERFORMER'),
        Token(9, TokenType.WS, ' '),
        Token(9, TokenType.QSTR, 'The Rolling Stones'),
        Token(9, TokenType.EOL, '\n'),
        #
        Token(10, TokenType.WS, '    '),
        Token(10, TokenType.NAME, 'INDEX'),
        Token(10, TokenType.WS, ' '),
        Token(10, TokenType.INT, 1),
        Token(10, TokenType.WS, ' '),
        Token(10, TokenType.IDX_PT, IndexPoint(0, 0, 0)),
        Token(10, TokenType.EOL, '\n'),
        #
        Token(11, TokenType.WS, '  '),
        Token(11, TokenType.NAME, 'TRACK'),
        Token(11, TokenType.WS, ' '),
        Token(11, TokenType.INT, 2),
        Token(11, TokenType.WS, ' '),
        Token(11, TokenType.NAME, 'AUDIO'),
        Token(11, TokenType.EOL, '\n'),
        #
        Token(12, TokenType.WS, '    '),
        Token(12, TokenType.NAME, 'TITLE'),
        Token(12, TokenType.WS, ' '),
        Token(12, TokenType.QSTR, 'Love in Vain'),
        Token(12, TokenType.EOL, '\n'),
        #
        Token(13, TokenType.WS, '    '),
        Token(13, TokenType.NAME, 'PERFORMER'),
        Token(13, TokenType.WS, ' '),
        Token(13, TokenType.QSTR, 'The Rolling Stones'),
        Token(13, TokenType.EOL, '\n'),
        #
        Token(14, TokenType.WS, '    '),
        Token(14, TokenType.NAME, 'INDEX'),
        Token(14, TokenType.WS, ' '),
        Token(14, TokenType.INT, 0),
        Token(14, TokenType.WS, ' '),
        Token(14, TokenType.IDX_PT, IndexPoint(4, 31, 12)),
        Token(14, TokenType.EOL, '\n'),
        #
        Token(15, TokenType.WS, '    '),
        Token(15, TokenType.NAME, 'INDEX'),
        Token(15, TokenType.WS, ' '),
        Token(15, TokenType.INT, 1),
        Token(15, TokenType.WS, ' '),
        Token(15, TokenType.IDX_PT, IndexPoint(4, 32, 34)),
        Token(15, TokenType.EOL, '\n'),
    ]
    parser = Parser(iter(tokens))

    assert parser.parse() == Root(
        tokens=[],
        children=[
            Performer(
                tokens=[
                    Token(1, TokenType.QSTR, 'The Rolling Stones'),
                ],
                children=[],
            ),
            Title(
                tokens=[
                    Token(2, TokenType.QSTR, 'Let It Bleed'),
                ],
                children=[],
            ),
            Year(
                tokens=[
                    Token(3, TokenType.INT, 1969),
                ],
                children=[],
            ),
            Rem(
                tokens=[
                    Token(4, TokenType.NAME, 'GENRE'),
                    Token(4, TokenType.QSTR, 'Classic Rock'),
                ],
                children=[],
            ),
            File(
                tokens=[
                    Token(6, TokenType.QSTR, 'album.wav'),
                    Token(6, TokenType.NAME, 'WAVE'),
                ],
                children=[
                    Track(
                        tokens=[
                            Token(7, TokenType.INT, 1),
                            Token(7, TokenType.NAME, 'AUDIO'),
                        ],
                        children=[
                            Title(
                                tokens=[
                                    Token(8, TokenType.QSTR, 'Gimme Shelter'),
                                ],
                                children=[],
                            ),
                            Performer(
                                tokens=[
                                    Token(
                                        9, TokenType.QSTR, 'The Rolling Stones'
                                    ),
                                ],
                                children=[],
                            ),
                            Index(
                                tokens=[
                                    Token(10, TokenType.INT, 1),
                                    Token(
                                        10,
                                        TokenType.IDX_PT,
                                        IndexPoint(0, 0, 0),
                                    ),
                                ],
                                children=[],
                            ),
                        ],
                    ),
                    Track(
                        tokens=[
                            Token(11, TokenType.INT, 2),
                            Token(11, TokenType.NAME, 'AUDIO'),
                        ],
                        children=[
                            Title(
                                tokens=[
                                    Token(12, TokenType.QSTR, 'Love in Vain'),
                                ],
                                children=[],
                            ),
                            Performer(
                                tokens=[
                                    Token(
                                        13, TokenType.QSTR, 'The Rolling Stones'
                                    ),
                                ],
                                children=[],
                            ),
                            Index(
                                tokens=[
                                    Token(14, TokenType.INT, 0),
                                    Token(
                                        14,
                                        TokenType.IDX_PT,
                                        IndexPoint(4, 31, 12),
                                    ),
                                ],
                                children=[],
                            ),
                            Index(
                                tokens=[
                                    Token(15, TokenType.INT, 1),
                                    Token(
                                        15,
                                        TokenType.IDX_PT,
                                        IndexPoint(4, 32, 34),
                                    ),
                                ],
                                children=[],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
