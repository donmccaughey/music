import pytest

from .index import Index


@pytest.mark.parametrize(
    'index_string, expected_number, expected_minutes, expected_seconds, expected_frames',
    [
        ('INDEX 01 00:00:00', 1, 0, 0, 0),
        ('\n  INDEX \t 01  00:00:00 ', 1, 0, 0, 0),
        ('INDEX 00 04:20:38', 0, 4, 20, 38),
        ('INDEX 01 09:21:66', 1, 9, 21, 66),
    ],
)
def test_index_parse(
    index_string,
    expected_number,
    expected_minutes,
    expected_seconds,
    expected_frames,
):
    index = Index.parse(42, index_string)
    assert index
    assert index.line_number == 42
    assert index.line == index_string
    assert index.number == expected_number
    assert index.minutes == expected_minutes
    assert index.seconds == expected_seconds
    assert index.frames == expected_frames


@pytest.mark.parametrize(
    'index_string',
    [
        'INDEX: 01 00:00:00',
        'INDE 01 00:00:00',
        'INDEX 01 ',
        'INDEX 00:00:00',
        ' 01  00:00:00',
        'INDEX xx 04:20:38',
        'INDEX 01 09:21',
        'INDEX 01 09:21:xx',
        '   ',
        '',
    ],
)
def test_index_parse_fails(index_string):
    index = Index.parse(42, index_string)
    assert not index
