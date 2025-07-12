from typing import Iterator

from .token import Token
from .token_type import TokenType
from .tokens import chomp, is_blank_line, take_non_blank_line, take_line


def test_chomp():
    tokens: list[Token] = []
    assert chomp(tokens) == []

    tokens = [Token(1, TokenType.EOL, '\n')]
    assert chomp(tokens) == []

    tokens = [Token(2, TokenType.NAME, 'REM'), Token(2, TokenType.EOL, '\n')]
    assert chomp(tokens) == [Token(2, TokenType.NAME, 'REM')]


def test_is_blank_line():
    tokens: list[Token] = []
    assert not is_blank_line(tokens)

    tokens = [Token(1, TokenType.EOL, '\n')]
    assert is_blank_line(tokens)

    tokens = [Token(2, TokenType.NAME, 'REM'), Token(2, TokenType.EOL, '\n')]
    assert not is_blank_line(tokens)


def test_take_line_when_empty():
    token_iter: Iterator[Token] = iter([])
    assert take_line(token_iter) == []


def test_take_line_for_several_lines():
    token_iter = iter(
        [
            Token(1, TokenType.NAME, 'PERFORMER'),
            Token(1, TokenType.QSTR, 'The Rolling Stones'),
            Token(1, TokenType.EOL, '\n'),
            #
            Token(2, TokenType.NAME, 'TITLE'),
            Token(2, TokenType.QSTR, 'Gimme Shelter'),
            Token(2, TokenType.EOL, '\n'),
            #
            Token(3, TokenType.EOL, '\n'),
        ]
    )
    assert take_line(token_iter) == [
        Token(1, TokenType.NAME, 'PERFORMER'),
        Token(1, TokenType.QSTR, 'The Rolling Stones'),
        Token(1, TokenType.EOL, '\n'),
    ]
    assert take_line(token_iter) == [
        Token(2, TokenType.NAME, 'TITLE'),
        Token(2, TokenType.QSTR, 'Gimme Shelter'),
        Token(2, TokenType.EOL, '\n'),
    ]
    assert take_line(token_iter) == [Token(3, TokenType.EOL, '\n')]
    assert take_line(token_iter) == []


def test_take_line_for_missing_eol():
    token_iter = iter(
        [
            Token(1, TokenType.NAME, 'PERFORMER'),
            Token(1, TokenType.QSTR, 'The Rolling Stones'),
        ]
    )
    assert take_line(token_iter) == [
        Token(1, TokenType.NAME, 'PERFORMER'),
        Token(1, TokenType.QSTR, 'The Rolling Stones'),
    ]
    assert take_line(token_iter) == []


def test_take_non_blank_line_when_empty():
    token_iter: Iterator[Token] = iter([])
    assert take_non_blank_line(token_iter) == []


def test_take_non_blank_line_for_several_lines():
    token_iter = iter(
        [
            Token(1, TokenType.NAME, 'PERFORMER'),
            Token(1, TokenType.QSTR, 'The Rolling Stones'),
            Token(1, TokenType.EOL, '\n'),
            #
            Token(2, TokenType.EOL, '\n'),
            #
            Token(3, TokenType.NAME, 'TITLE'),
            Token(3, TokenType.QSTR, 'Gimme Shelter'),
            Token(3, TokenType.EOL, '\n'),
            #
            Token(4, TokenType.EOL, '\n'),
        ]
    )
    assert take_non_blank_line(token_iter) == [
        Token(1, TokenType.NAME, 'PERFORMER'),
        Token(1, TokenType.QSTR, 'The Rolling Stones'),
        Token(1, TokenType.EOL, '\n'),
    ]
    assert take_non_blank_line(token_iter) == [
        Token(3, TokenType.NAME, 'TITLE'),
        Token(3, TokenType.QSTR, 'Gimme Shelter'),
        Token(3, TokenType.EOL, '\n'),
    ]
    assert take_non_blank_line(token_iter) == []
