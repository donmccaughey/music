from typing import Iterator

from .token import Token
from .token_type import EOL, NAME, QSTR
from .tokens import chomp, is_blank_line, take_non_blank_line, take_line


def test_chomp():
    tokens: list[Token] = []
    assert chomp(tokens) == []

    tokens = [Token(1, EOL, '\n')]
    assert chomp(tokens) == []

    tokens = [Token(2, NAME, 'REM'), Token(2, EOL, '\n')]
    assert chomp(tokens) == [Token(2, NAME, 'REM')]


def test_is_blank_line():
    tokens: list[Token] = []
    assert not is_blank_line(tokens)

    tokens = [Token(1, EOL, '\n')]
    assert is_blank_line(tokens)

    tokens = [Token(2, NAME, 'REM'), Token(2, EOL, '\n')]
    assert not is_blank_line(tokens)


def test_take_line_when_empty():
    token_iter: Iterator[Token] = iter([])
    assert take_line(token_iter) == []


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
    assert take_line(token_iter) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
        Token(1, EOL, '\n'),
    ]
    assert take_line(token_iter) == [
        Token(2, NAME, 'TITLE'),
        Token(2, QSTR, 'Gimme Shelter'),
        Token(2, EOL, '\n'),
    ]
    assert take_line(token_iter) == [Token(3, EOL, '\n')]
    assert take_line(token_iter) == []


def test_take_line_for_missing_eol():
    token_iter = iter(
        [
            Token(1, NAME, 'PERFORMER'),
            Token(1, QSTR, 'The Rolling Stones'),
        ]
    )
    assert take_line(token_iter) == [
        Token(1, NAME, 'PERFORMER'),
        Token(1, QSTR, 'The Rolling Stones'),
    ]
    assert take_line(token_iter) == []


def test_take_non_blank_line_when_empty():
    token_iter: Iterator[Token] = iter([])
    assert take_non_blank_line(token_iter) == []


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
    assert take_non_blank_line(token_iter) == []
