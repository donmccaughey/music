from typing import Iterator

from .token import Token
from .token_type import EOL, INT, NAME, QSTR
from .tokens import take_non_blank_lines, take_lines


def test_take_lines_when_empty():
    token_iter: Iterator[Token] = iter([])
    lines = take_lines(token_iter)
    assert next(lines, None) is None


def test_take_lines_for_several_lines():
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
    lines = take_lines(token_iter)
    assert next(lines) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert next(lines) == [
        Token(2, NAME, 'TITLE'),
        Token(2, QSTR, 'Gimme Shelter'),
    ]
    assert next(lines) == []
    assert next(lines, None) is None


def test_take_lines_for_missing_eol():
    token_iter = iter(
        [
            Token(1, NAME, 'PERFORMER'),
            Token(1, QSTR, 'The Rolling Stones'),
        ]
    )
    lines = take_lines(token_iter)
    assert next(lines) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert next(lines, None) is None


def test_take_non_blank_lines_when_empty():
    token_iter: Iterator[Token] = iter([])
    non_blank_lines = take_non_blank_lines(token_iter)
    assert next(non_blank_lines, None) is None


def test_take_non_blank_lines_for_one_blank_line():
    token_iter = iter([Token(1, EOL, '\n')])
    non_blank_lines = take_non_blank_lines(token_iter)
    assert next(non_blank_lines, None) is None


def test_take_non_blank_lines_for_several_lines():
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
    non_blank_lines = take_non_blank_lines(token_iter)
    assert next(non_blank_lines) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert next(non_blank_lines) == [
        Token(3, NAME, 'TITLE'),
        Token(3, QSTR, 'Gimme Shelter'),
    ]
    assert next(non_blank_lines, None) is None


def test_take_non_blank_lines_for_many_blank_lines():
    token_iter = iter(
        [
            Token(1, NAME, 'PERFORMER'),
            Token(1, QSTR, 'The Rolling Stones'),
            Token(1, EOL, '\n'),
            #
            Token(2, EOL, '\n'),
            #
            Token(3, EOL, '\n'),
            #
            Token(4, EOL, '\n'),
            #
            Token(5, NAME, 'TITLE'),
            Token(5, QSTR, 'Gimme Shelter'),
            Token(5, EOL, '\n'),
            #
            Token(6, EOL, '\n'),
        ]
    )
    non_blank_lines = take_non_blank_lines(token_iter)
    assert next(non_blank_lines) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert next(non_blank_lines) == [
        Token(5, NAME, 'TITLE'),
        Token(5, QSTR, 'Gimme Shelter'),
    ]
    assert next(non_blank_lines, None) is None
