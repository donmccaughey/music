import pytest
from .performer import Performer


@pytest.mark.parametrize(
    'performer_string, expected_name',
    [
        ('PERFORMER "Alice"', 'Alice'),
        ('PERFORMER "Alice and Bob"', 'Alice and Bob'),
        ('  PERFORMER \t "  Alice  and Bob  "', 'Alice and Bob'),
    ]
)
def test_performer_parse_fails(performer_string, expected_name):
    performer = Performer.parse(performer_string)
    assert performer is not None
    assert performer.name == expected_name


@pytest.mark.parametrize('performer_string', [
    'PERFORMER: "Alice"',
    'ERFORMER "Bob"',
    '"Carlos"',
    '   ',
    '',
])
def test_performer_parse(performer_string):
    performer = Performer.parse(performer_string)
    assert performer is None
