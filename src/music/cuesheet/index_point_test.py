import pytest

from .index_point import IndexPoint


@pytest.mark.parametrize(
    'text, expected',
    [
        ('01:23:45', IndexPoint(1, 23, 45)),
        ('01:23:4', None),
        ('1:23:45', None),
        ('01:23:456', None),
        ('01.23.45', None),
        ('o1:23:45', None),
        ('01:2e:45', None),
        ('01:23:4a', None),
    ],
)
def test_parse(text, expected):
    assert IndexPoint.parse(text) == expected
