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
    title = Title.parse(42, title_string)
    assert title is not None
    assert title.line_number == 42
    assert title.line == title_string
    assert title.title == expected_title


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
    title = Title.parse(42, title_string)
    assert title is None
