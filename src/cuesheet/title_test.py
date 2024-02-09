import pytest
from .title import Title


@pytest.mark.parametrize(
    'title_string, expected_title',
    [
        ('TITLE "Hello"', 'Hello'),
        ('TITLE "Hello, World!"', 'Hello, World!'),
        ('  TITLE \t "  Hello,  World!  "', 'Hello, World!'),
    ]
)
def test_performer_parse_fails(title_string, expected_title):
    performer = Title.parse(title_string)
    assert performer is not None
    assert performer.title == expected_title


@pytest.mark.parametrize('title_string', [
    'TITLE: "Once"',
    'TITLE Twice"',
    'TITLE "Thrice',
    'TTLE "Mice"',
    '"Cat"',
    '   ',
    '',
])
def test_performer_parse(title_string):
    performer = Title.parse(title_string)
    assert performer is None
