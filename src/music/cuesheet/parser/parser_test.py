from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .file import File
from .parser import Parser
from .performer import Performer
from .root import Root
from .title import Title
from .track import Track


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
        Token(3, TokenType.WS, ' '),
        Token(3, TokenType.EOL, '\n'),
        #
        Token(4, TokenType.NAME, 'FILE'),
        Token(4, TokenType.WS, ' '),
        Token(4, TokenType.QSTR, 'album.wav'),
        Token(4, TokenType.WS, ' '),
        Token(4, TokenType.NAME, 'WAVE'),
        Token(4, TokenType.EOL, '\n'),
        #
        Token(5, TokenType.WS, '  '),
        Token(5, TokenType.NAME, 'TRACK'),
        Token(5, TokenType.WS, ' '),
        Token(5, TokenType.INT, 1),
        Token(5, TokenType.WS, ' '),
        Token(5, TokenType.NAME, 'AUDIO'),
        Token(5, TokenType.EOL, '\n'),
        #
        Token(6, TokenType.WS, '    '),
        Token(6, TokenType.NAME, 'TITLE'),
        Token(6, TokenType.WS, ' '),
        Token(6, TokenType.QSTR, 'Gimme Shelter'),
        Token(6, TokenType.EOL, '\n'),
        #
        Token(7, TokenType.WS, '    '),
        Token(7, TokenType.NAME, 'PERFORMER'),
        Token(7, TokenType.WS, ' '),
        Token(7, TokenType.QSTR, 'The Rolling Stones'),
        Token(7, TokenType.EOL, '\n'),
        #
        Token(9, TokenType.WS, '  '),
        Token(9, TokenType.NAME, 'TRACK'),
        Token(9, TokenType.WS, ' '),
        Token(9, TokenType.INT, 2),
        Token(9, TokenType.WS, ' '),
        Token(9, TokenType.NAME, 'AUDIO'),
        Token(9, TokenType.EOL, '\n'),
        #
        Token(10, TokenType.WS, '    '),
        Token(10, TokenType.NAME, 'TITLE'),
        Token(10, TokenType.WS, ' '),
        Token(10, TokenType.QSTR, 'Love in Vain'),
        Token(10, TokenType.EOL, '\n'),
        #
        Token(11, TokenType.WS, '    '),
        Token(11, TokenType.NAME, 'PERFORMER'),
        Token(11, TokenType.WS, ' '),
        Token(11, TokenType.QSTR, 'The Rolling Stones'),
        Token(11, TokenType.EOL, '\n'),
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
            File(
                tokens=[
                    Token(4, TokenType.QSTR, 'album.wav'),
                    Token(4, TokenType.NAME, 'WAVE'),
                ],
                children=[
                    Track(
                        tokens=[
                            Token(5, TokenType.INT, 1),
                            Token(5, TokenType.NAME, 'AUDIO'),
                        ],
                        children=[
                            Title(
                                tokens=[
                                    Token(6, TokenType.QSTR, 'Gimme Shelter'),
                                ],
                                children=[],
                            ),
                            Performer(
                                tokens=[
                                    Token(
                                        7, TokenType.QSTR, 'The Rolling Stones'
                                    ),
                                ],
                                children=[],
                            ),
                        ],
                    ),
                    Track(
                        tokens=[
                            Token(9, TokenType.INT, 2),
                            Token(9, TokenType.NAME, 'AUDIO'),
                        ],
                        children=[
                            Title(
                                tokens=[
                                    Token(10, TokenType.QSTR, 'Love in Vain'),
                                ],
                                children=[],
                            ),
                            Performer(
                                tokens=[
                                    Token(
                                        11, TokenType.QSTR, 'The Rolling Stones'
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
