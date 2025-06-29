import pytest

from .track import Track


@pytest.mark.parametrize(
    'track_string, expected_number, expected_track_type',
    [
        ('TRACK 01 AUDIO', 1, 'AUDIO'),
        ('\n  TRACK \t01   AUDIO\n', 1, 'AUDIO'),
    ],
)
def test_track_parse(track_string, expected_number, expected_track_type):
    track = Track.parse(42, track_string)
    assert track
    assert track.line_number == 42
    assert track.line == track_string
    assert track.number == expected_number
    assert track.track_type == expected_track_type
    assert not track.title
    assert not track.performer
    assert track.indices == []


@pytest.mark.parametrize(
    'track_string',
    [
        'TRACK 01',
        'CRACK 01 AUDIO',
        'TRACK one AUDIO',
        '   ',
        '',
    ],
)
def test_track_parse_fails(track_string):
    track = Track.parse(42, track_string)
    assert not track
