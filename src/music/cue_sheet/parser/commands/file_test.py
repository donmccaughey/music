from pathlib import Path

from music.cue_sheet.lexer import EOL, NAME, QSTR, Token

from .file import File


def test_is_file_with_type():
    tokens = [
        Token(4, NAME, 'FILE'),
        Token(4, QSTR, 'Hard Candy'),
        Token(4, NAME, 'WAVE'),
        Token(4, EOL, '\n'),
    ]
    assert File.is_file(tokens)
    assert File.is_file_with_type(tokens)
    assert not File.is_file_without_type(tokens)


def test_is_file_without_type():
    tokens = [
        Token(4, NAME, 'FILE'),
        Token(4, QSTR, 'Hard Candy'),
        Token(4, EOL, '\n'),
    ]
    assert File.is_file(tokens)
    assert not File.is_file_with_type(tokens)
    assert File.is_file_without_type(tokens)


def test_parse_with_type():
    tokens = [
        Token(4, NAME, 'FILE'),
        Token(4, QSTR, 'Hard Candy'),
        Token(4, NAME, 'WAVE'),
        Token(4, EOL, '\n'),
    ]
    file = File.parse(tokens)
    assert file
    assert file.filename == Path('Hard Candy')
    assert file.type == 'WAVE'


def test_parse_without_type():
    tokens = [
        Token(4, NAME, 'FILE'),
        Token(4, QSTR, 'Hard Candy'),
        Token(4, EOL, '\n'),
    ]
    file = File.parse(tokens)
    assert file
    assert file.filename == Path('Hard Candy')
    assert file.type == 'WAVE'
