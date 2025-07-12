from .token import Token
from .token_type import EOL, STR, WS


def test_bool_properties():
    token = Token(1, WS, ' ')
    assert not token.is_end_of_line
    assert token.is_whitespace

    token = Token(1, EOL, ' ')
    assert token.is_end_of_line
    assert not token.is_whitespace

    token = Token(1, STR, 'foobar')
    assert not token.is_end_of_line
    assert not token.is_whitespace
