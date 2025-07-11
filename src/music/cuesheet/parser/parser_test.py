from music.cuesheet import IndexPoint
from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .asin import ASIN
from .comment import Comment
from .disc_id import DiscID
from .file import File
from .genre import Genre
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
        Token(5, TokenType.NAME, 'REM'),
        Token(5, TokenType.WS, ' '),
        Token(5, TokenType.NAME, 'ASIN'),
        Token(5, TokenType.WS, ' '),
        Token(5, TokenType.STR, 'B00006ZCFG'),
        Token(5, TokenType.EOL, '\n'),
        #
        Token(6, TokenType.NAME, 'REM'),
        Token(6, TokenType.WS, ' '),
        Token(6, TokenType.NAME, 'DISCID'),
        Token(6, TokenType.WS, ' '),
        Token(6, TokenType.STR, '9E0B010C'),
        Token(6, TokenType.EOL, '\n'),
        #
        Token(7, TokenType.NAME, 'REM'),
        Token(7, TokenType.WS, ' '),
        Token(7, TokenType.NAME, 'COMMENT'),
        Token(7, TokenType.WS, ' '),
        Token(7, TokenType.QSTR, 'ExactAudioCopy v0.95b4'),
        Token(7, TokenType.EOL, '\n'),
        #
        Token(8, TokenType.NAME, 'REM'),
        Token(8, TokenType.WS, ' '),
        Token(8, TokenType.QSTR, 'This is a remark'),
        Token(8, TokenType.EOL, '\n'),
        #
        Token(9, TokenType.NAME, 'FILE'),
        Token(9, TokenType.WS, ' '),
        Token(9, TokenType.QSTR, 'album.wav'),
        Token(9, TokenType.WS, ' '),
        Token(9, TokenType.NAME, 'WAVE'),
        Token(9, TokenType.EOL, '\n'),
        #
        Token(10, TokenType.WS, '  '),
        Token(10, TokenType.NAME, 'TRACK'),
        Token(10, TokenType.WS, ' '),
        Token(10, TokenType.INT, 1),
        Token(10, TokenType.WS, ' '),
        Token(10, TokenType.NAME, 'AUDIO'),
        Token(10, TokenType.EOL, '\n'),
        #
        Token(11, TokenType.WS, '    '),
        Token(11, TokenType.NAME, 'TITLE'),
        Token(11, TokenType.WS, ' '),
        Token(11, TokenType.QSTR, 'Gimme Shelter'),
        Token(11, TokenType.EOL, '\n'),
        #
        Token(12, TokenType.WS, '    '),
        Token(12, TokenType.NAME, 'PERFORMER'),
        Token(12, TokenType.WS, ' '),
        Token(12, TokenType.QSTR, 'The Rolling Stones'),
        Token(12, TokenType.EOL, '\n'),
        #
        Token(13, TokenType.WS, '    '),
        Token(13, TokenType.NAME, 'INDEX'),
        Token(13, TokenType.WS, ' '),
        Token(13, TokenType.INT, 1),
        Token(13, TokenType.WS, ' '),
        Token(13, TokenType.IDX_PT, IndexPoint(0, 0, 0)),
        Token(13, TokenType.EOL, '\n'),
        #
        Token(14, TokenType.WS, '  '),
        Token(14, TokenType.NAME, 'TRACK'),
        Token(14, TokenType.WS, ' '),
        Token(14, TokenType.INT, 2),
        Token(14, TokenType.WS, ' '),
        Token(14, TokenType.NAME, 'AUDIO'),
        Token(14, TokenType.EOL, '\n'),
        #
        Token(15, TokenType.WS, '    '),
        Token(15, TokenType.NAME, 'TITLE'),
        Token(15, TokenType.WS, ' '),
        Token(15, TokenType.QSTR, 'Love in Vain'),
        Token(15, TokenType.EOL, '\n'),
        #
        Token(16, TokenType.WS, '    '),
        Token(16, TokenType.NAME, 'PERFORMER'),
        Token(16, TokenType.WS, ' '),
        Token(16, TokenType.QSTR, 'The Rolling Stones'),
        Token(16, TokenType.EOL, '\n'),
        #
        Token(17, TokenType.WS, '    '),
        Token(17, TokenType.NAME, 'INDEX'),
        Token(17, TokenType.WS, ' '),
        Token(17, TokenType.INT, 0),
        Token(17, TokenType.WS, ' '),
        Token(17, TokenType.IDX_PT, IndexPoint(4, 31, 12)),
        Token(17, TokenType.EOL, '\n'),
        #
        Token(18, TokenType.WS, '    '),
        Token(18, TokenType.NAME, 'INDEX'),
        Token(18, TokenType.WS, ' '),
        Token(18, TokenType.INT, 1),
        Token(18, TokenType.WS, ' '),
        Token(18, TokenType.IDX_PT, IndexPoint(4, 32, 34)),
        Token(18, TokenType.EOL, '\n'),
        #
        Token(19, TokenType.WS, ' '),
        Token(19, TokenType.EOL, '\n'),
        #
        Token(20, TokenType.WS, ' '),
        Token(20, TokenType.EOL, '\n'),
    ]
    parser = Parser(iter(tokens))

    assert parser.parse() == Root(
        [
            Performer(
                tokens=[
                    Token(1, TokenType.NAME, 'PERFORMER'),
                    Token(1, TokenType.QSTR, 'The Rolling Stones'),
                    Token(1, TokenType.EOL, '\n'),
                ],
            ),
            Title(
                tokens=[
                    Token(2, TokenType.NAME, 'TITLE'),
                    Token(2, TokenType.QSTR, 'Let It Bleed'),
                    Token(2, TokenType.EOL, '\n'),
                ],
            ),
            Year(
                tokens=[
                    Token(3, TokenType.INT, 1969),
                ],
            ),
            Genre(
                tokens=[
                    Token(4, TokenType.QSTR, 'Classic Rock'),
                ],
            ),
            ASIN(
                tokens=[
                    Token(5, TokenType.STR, 'B00006ZCFG'),
                ],
            ),
            DiscID(
                tokens=[
                    Token(6, TokenType.STR, '9E0B010C'),
                ],
            ),
            Comment(
                tokens=[
                    Token(7, TokenType.QSTR, 'ExactAudioCopy v0.95b4'),
                ],
            ),
            Rem(
                tokens=[
                    Token(8, TokenType.QSTR, 'This is a remark'),
                ],
            ),
            File(
                tokens=[
                    Token(9, TokenType.NAME, 'FILE'),
                    Token(9, TokenType.QSTR, 'album.wav'),
                    Token(9, TokenType.NAME, 'WAVE'),
                    Token(9, TokenType.EOL, '\n'),
                ],
                children=[
                    Track(
                        tokens=[
                            Token(10, TokenType.INT, 1),
                            Token(10, TokenType.NAME, 'AUDIO'),
                        ],
                        children=[
                            Title(
                                tokens=[
                                    Token(11, TokenType.NAME, 'TITLE'),
                                    Token(11, TokenType.QSTR, 'Gimme Shelter'),
                                    Token(11, TokenType.EOL, '\n'),
                                ],
                            ),
                            Performer(
                                tokens=[
                                    Token(12, TokenType.NAME, 'PERFORMER'),
                                    Token(
                                        12, TokenType.QSTR, 'The Rolling Stones'
                                    ),
                                    Token(12, TokenType.EOL, '\n'),
                                ],
                            ),
                            Index(
                                tokens=[
                                    Token(13, TokenType.INT, 1),
                                    Token(
                                        13,
                                        TokenType.IDX_PT,
                                        IndexPoint(0, 0, 0),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Track(
                        tokens=[
                            Token(14, TokenType.INT, 2),
                            Token(14, TokenType.NAME, 'AUDIO'),
                        ],
                        children=[
                            Title(
                                tokens=[
                                    Token(15, TokenType.NAME, 'TITLE'),
                                    Token(15, TokenType.QSTR, 'Love in Vain'),
                                    Token(15, TokenType.EOL, '\n'),
                                ],
                            ),
                            Performer(
                                tokens=[
                                    Token(16, TokenType.NAME, 'PERFORMER'),
                                    Token(
                                        16, TokenType.QSTR, 'The Rolling Stones'
                                    ),
                                    Token(16, TokenType.EOL, '\n'),
                                ],
                            ),
                            Index(
                                tokens=[
                                    Token(17, TokenType.INT, 0),
                                    Token(
                                        17,
                                        TokenType.IDX_PT,
                                        IndexPoint(4, 31, 12),
                                    ),
                                ],
                            ),
                            Index(
                                tokens=[
                                    Token(18, TokenType.INT, 1),
                                    Token(
                                        18,
                                        TokenType.IDX_PT,
                                        IndexPoint(4, 32, 34),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
