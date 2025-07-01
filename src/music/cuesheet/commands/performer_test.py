import pytest

from music.cuesheet.lexer.line import Line

from .performer import Performer


@pytest.mark.parametrize(
    'performer_string, expected_name',
    [
        ('PERFORMER "Alice"', 'Alice'),
        ('PERFORMER "Alice and Bob"', 'Alice and Bob'),
        ('  PERFORMER \t "  Alice  and Bob  "', 'Alice and Bob'),
    ],
)
def test_performer_parse(performer_string, expected_name):
    performer = Performer.parse(Line(42, performer_string))
    assert performer
    assert performer.line == Line(42, performer_string)
    assert performer.name == expected_name


@pytest.mark.parametrize(
    'performer_string',
    [
        'PERFORMER: "Alice"',
        'PERFORMER Bob"',
        'PERFORMER "Carlos',
        'ERFORMER "Davina"',
        '"Ed"',
        '   ',
        '',
    ],
)
def test_performer_parse_fails(performer_string):
    performer = Performer.parse(Line(42, performer_string))
    assert not performer
