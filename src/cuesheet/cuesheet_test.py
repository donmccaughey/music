from pathlib import Path
from textwrap import dedent

import pytest

from .cuesheet import CueSheet

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_data'


def test_parse():
    cue_sheet = CueSheet.parse(read_test_data('cue_sheet1.txt'))
    assert cue_sheet
    assert cue_sheet.performer
    assert cue_sheet.performer.name == '3 Doors Down'
    assert cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'
    assert cue_sheet.file
    assert cue_sheet.file.filename == Path('album.wav')
    assert cue_sheet.file.file_type == 'WAVE'
    assert len(cue_sheet.file.tracks) == 12

    track1 = cue_sheet.file.tracks[0]
    assert track1.number == 1
    assert track1.track_type == 'AUDIO'
    assert track1.title
    assert track1.title.title == "When I'm Gone"
    assert track1.performer
    assert track1.performer.name == '3 Doors Down'
    assert len(track1.indices) == 1

    index1 = track1.indices[0]
    assert index1.number == 1
    assert index1.minutes == 0
    assert index1.seconds == 0
    assert index1.frames == 0

    track12 = cue_sheet.file.tracks[-1]
    assert track12.number == 12
    assert track12.track_type == 'AUDIO'
    assert track12.title
    assert track12.title.title == "This Time"
    assert track12.performer
    assert track12.performer.name == '3 Doors Down'
    assert len(track1.indices) == 1

    index1 = track12.indices[0]
    assert index1.number == 1
    assert index1.minutes == 41
    assert index1.seconds == 38
    assert index1.frames == 70

    assert not cue_sheet.errors


def test_parse_blank():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        
        FILE "album.wav" WAVE
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert not cue_sheet.errors


def test_parse_error():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        NOTACOMMAND fnord
        FILE "album.wav" WAVE
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 3
    assert cue_sheet.errors[0].line == 'NOTACOMMAND fnord'


def test_parse_index():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TRACK 02 AUDIO
                INDEX 00 04:20:38
                INDEX 01 04:21:66
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet and cue_sheet.file and cue_sheet.file.tracks
    assert cue_sheet.file.tracks[0].indices
    assert len(cue_sheet.file.tracks[0].indices) == 2

    index0 = cue_sheet.file.tracks[0].indices[0]
    assert index0.number == 0
    assert index0.minutes == 4
    assert index0.seconds == 20
    assert index0.frames == 38

    index1 = cue_sheet.file.tracks[0].indices[1]
    assert index1.number == 1
    assert index1.minutes == 4
    assert index1.seconds == 21
    assert index1.frames == 66


@pytest.mark.skip
def test_parse_index_duplicate_number():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TRACK 02 AUDIO
                INDEX 00 04:20:38
                INDEX 00 04:21:66
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet and cue_sheet.file and cue_sheet.file.tracks
    assert cue_sheet.file.tracks[0].indices
    assert len(cue_sheet.file.tracks[0].indices) == 1
    assert len(cue_sheet.errors) == 1

    index0 = cue_sheet.file.tracks[0].indices[0]
    assert index0.number == 0
    assert index0.minutes == 4
    assert index0.seconds == 20
    assert index0.frames == 38

    assert cue_sheet.errors[0].line_number == 6
    assert cue_sheet.errors[0].line == 'INDEX 00 04:21:66'


def test_parse_index_misplaced_in_head():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        INDEX 01 00:00:00
        FILE "album.wav" WAVE
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 3
    assert cue_sheet.errors[0].line == 'INDEX 01 00:00:00'


def test_parse_index_misplaced_in_file():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            INDEX 01 00:00:00
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 4
    assert cue_sheet.errors[0].line == '    INDEX 01 00:00:00'


def test_parse_performer_misplaced():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            PERFORMER "3 Doors Down"
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 4
    assert cue_sheet.errors[0].line == '    PERFORMER "3 Doors Down"'


def test_parse_remark():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        REM foo bar
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert len(cue_sheet.remarks) == 1
    assert cue_sheet.remarks[0].remark == 'foo bar'
    assert not cue_sheet.errors


def test_parse_remark_in_file():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            REM foo bar
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert not cue_sheet.remarks
    assert cue_sheet.file and cue_sheet.file.remarks
    assert cue_sheet.file.remarks[0].remark == 'foo bar'
    assert not cue_sheet.errors


def test_parse_remark_in_track():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TRACK 01 AUDIO
                REM foo bar
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert not cue_sheet.remarks
    assert cue_sheet.file and not cue_sheet.file.remarks
    assert cue_sheet.file.tracks and cue_sheet.file.tracks[0].remarks
    assert cue_sheet.file.tracks[0].remarks[0].remark == 'foo bar'
    assert not cue_sheet.errors


def test_parse_title_misplaced():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TITLE "Away From The Sun"
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet and cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'

    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 4
    assert cue_sheet.errors[0].line == '    TITLE "Away From The Sun"'


def test_parse_track_misplaced():
    s = make_test_data('''
        PERFORMER "3 Doors Down"
        TRACK 01 AUDIO
        TITLE "Away From The Sun"
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 2
    assert cue_sheet.errors[0].line == 'TRACK 01 AUDIO'


def read_test_data(filename: str) -> str:
    path = TEST_DATA_DIR / filename
    return path.read_text()


def make_test_data(s: str) -> str:
    return dedent(s).lstrip()
