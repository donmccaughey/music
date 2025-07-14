from typing import Iterator

from .token import Token
from .token_type import EOL, NAME, QSTR
from .tokens import take_non_blank_line, take_line


def test_take_line_when_empty():
    token_iter: Iterator[Token] = iter([])
    assert next(take_line(token_iter), None) is None


def test_take_line_for_several_lines():
    token_iter = iter(
        [
            Token(1, NAME, 'PERFORMER'),
            Token(1, QSTR, 'The Rolling Stones'),
            Token(1, EOL, '\n'),
            #
            Token(2, NAME, 'TITLE'),
            Token(2, QSTR, 'Gimme Shelter'),
            Token(2, EOL, '\n'),
            #
            Token(3, EOL, '\n'),
        ]
    )
    assert next(take_line(token_iter)) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert next(take_line(token_iter)) == [
        Token(2, NAME, 'TITLE'),
        Token(2, QSTR, 'Gimme Shelter'),
    ]
    assert next(take_line(token_iter)) == []
    assert next(take_line(token_iter), None) is None


def test_take_line_for_missing_eol():
    token_iter = iter(
        [
            Token(1, NAME, 'PERFORMER'),
            Token(1, QSTR, 'The Rolling Stones'),
        ]
    )
    assert next(take_line(token_iter)) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert next(take_line(token_iter), None) is None


def test_take_non_blank_line_when_empty():
    token_iter: Iterator[Token] = iter([])
    assert take_non_blank_line(token_iter) is None


def test_take_non_blank_line_for_one_blank_line():
    token_iter = iter([Token(1, EOL, '\n')])
    assert take_non_blank_line(token_iter) is None


def test_take_non_blank_line_for_several_lines():
    token_iter = iter(
        [
            Token(1, NAME, 'PERFORMER'),
            Token(1, QSTR, 'The Rolling Stones'),
            Token(1, EOL, '\n'),
            #
            Token(2, EOL, '\n'),
            #
            Token(3, NAME, 'TITLE'),
            Token(3, QSTR, 'Gimme Shelter'),
            Token(3, EOL, '\n'),
            #
            Token(4, EOL, '\n'),
        ]
    )
    assert take_non_blank_line(token_iter) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert take_non_blank_line(token_iter) == [
        Token(3, NAME, 'TITLE'),
        Token(3, QSTR, 'Gimme Shelter'),
    ]
    assert take_non_blank_line(token_iter) is None
