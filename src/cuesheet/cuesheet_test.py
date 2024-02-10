from pathlib import Path
from textwrap import dedent

from .cuesheet import CueSheet

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_data'


def test_cue_sheet_parse():
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


def test_misplaced_index():
    s = unindent('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        INDEX 01 00:00:00
        FILE "album.wav" WAVE
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'

    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 3
    assert cue_sheet.errors[0].line == 'INDEX 01 00:00:00'


def test_misplaced_performer():
    s = unindent('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            PERFORMER "3 Doors Down"
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'

    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 4
    assert cue_sheet.errors[0].line == '    PERFORMER "3 Doors Down"'


def test_misplaced_title():
    s = unindent('''
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TITLE "Away From The Sun"
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'

    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 4
    assert cue_sheet.errors[0].line == '    TITLE "Away From The Sun"'


def test_misplaced_track():
    s = unindent('''
        PERFORMER "3 Doors Down"
        TRACK 01 AUDIO
        TITLE "Away From The Sun"
    ''')
    cue_sheet = CueSheet.parse(s)
    assert cue_sheet
    assert cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'

    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0].line_number == 2
    assert cue_sheet.errors[0].line == 'TRACK 01 AUDIO'


def read_test_data(filename: str) -> str:
    path = TEST_DATA_DIR / filename
    return path.read_text()


def unindent(s: str) -> str:
    return dedent(s).lstrip()
