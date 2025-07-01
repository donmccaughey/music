from pathlib import Path

import pytest

from music.cuesheet.lexer.line import Line

from .file import File


@pytest.mark.parametrize(
    'file_string, expected_filename, expected_file_type',
    [
        ('FILE "album.wav" WAVE', Path('album.wav'), 'WAVE'),
        ('\n  FILE \t"album.wav"   WAVE\n', Path('album.wav'), 'WAVE'),
        ('FILE "album.wav"', Path('album.wav'), None),
    ],
)
def test_file_parse(file_string, expected_filename, expected_file_type):
    file = File.parse(Line(42, file_string))
    assert file
    assert file.line == Line(42, file_string)
    assert file.filename == expected_filename
    assert file.file_type == expected_file_type
    assert file.tracks == []


@pytest.mark.parametrize(
    'file_string',
    [
        'FILE: "album.wav" WAVE',
        'FIL "album.wav" WAVE',
        'FILE WAVE',
        'FILE album.wav WAVE',
        '   ',
        '',
    ],
)
def test_file_parse_fails(file_string):
    file = File.parse(Line(42, file_string))
    assert not file
