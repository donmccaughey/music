import pytest
from .index import Index


@pytest.mark.parametrize(
    'index_string, expected_i, expected_minutes, expected_seconds, expected_frames',
[
    ('INDEX 01 00:00:00', 1, 0, 0, 0),
    ('\n  INDEX \t 01  00:00:00 ', 1, 0, 0, 0),
    ('INDEX 00 04:20:38', 0, 4, 20, 38),
    ('INDEX 01 04:21:66', 1, 4, 21, 66),
    # TODO: failure modes
])
def test_index_parse(index_string, expected_i, expected_minutes, expected_seconds, expected_frames):
    i, index = Index.parse(index_string)
    assert i == expected_i
    assert index.minutes == expected_minutes
    assert index.seconds == expected_seconds
    assert index.frames == expected_frames
