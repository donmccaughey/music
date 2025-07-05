import pytest

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .parser import Parser
from .performer import Performer
from .root import Root


@pytest.mark.parametrize(
    'tokens, expected',
    [
        (
            [
                Token(1, TokenType.NAME, 'PERFORMER'),
                Token(1, TokenType.QSTR, 'The Rolling Stones'),
                Token(1, TokenType.EOL, '\n'),
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
                ]
            ),
        ),
    ],
)
def test_parser(tokens, expected):
    tokens = [
        Token(1, TokenType.NAME, 'PERFORMER'),
        Token(1, TokenType.QSTR, 'The Rolling Stones'),
        Token(1, TokenType.EOL, '\n'),
    ]
    parser = Parser(iter(tokens))

    expected = Root(children=[Performer(tokens)])

    assert parser.parse() == expected
