from io import StringIO
from pathlib import Path
from textwrap import dedent

import pytest

from .builder import Builder
from .cue_sheet import CueSheet, CueSheet2
from .commands import Error
from .lexer.line import Line
from .lexer.lexer import Lexer
from .parser import Parser

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_data'


def test_parse():
    cue_sheet = CueSheet.parse(read_test_data('cuesheet.txt'))
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
    assert track12.title.title == 'This Time'
    assert track12.performer
    assert track12.performer.name == '3 Doors Down'
    assert len(track1.indices) == 1

    index1 = track12.indices[0]
    assert index1.number == 1
    assert index1.minutes == 41
    assert index1.seconds == 38
    assert index1.frames == 70

    assert not cue_sheet.errors


def test_parse_minimal():
    source = """
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        
        FILE "album.wav" WAVE
    """
    cue_sheet = parse_str(source)
    assert cue_sheet
    assert cue_sheet.performer
    assert cue_sheet
    assert not cue_sheet.errors


def test_parse_error():
    source = """
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        NOTACOMMAND fnord
        FILE "album.wav" WAVE
    """
    cue_sheet = parse_str(source)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0] == (3, 'NOTACOMMAND fnord')


def test_parse_index():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TRACK 02 AUDIO
                INDEX 00 04:20:38
                INDEX 01 04:21:66
    """)
    cue_sheet = CueSheet.parse(source)
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
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TRACK 02 AUDIO
                INDEX 00 04:20:38
                INDEX 00 04:21:66
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet and cue_sheet.file and cue_sheet.file.tracks
    assert cue_sheet.file.tracks[0].indices
    assert len(cue_sheet.file.tracks[0].indices) == 1
    assert len(cue_sheet.errors) == 1

    index0 = cue_sheet.file.tracks[0].indices[0]
    assert index0.number == 0
    assert index0.minutes == 4
    assert index0.seconds == 20
    assert index0.frames == 38

    assert cue_sheet.errors[0] == Error(Line(6, 'INDEX 00 04:21:66'))


def test_parse_index_misplaced_in_head():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        INDEX 01 00:00:00
        FILE "album.wav" WAVE
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0] == Error(Line(3, 'INDEX 01 00:00:00'))


def test_parse_index_misplaced_in_file():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            INDEX 01 00:00:00
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0] == Error(Line(4, '    INDEX 01 00:00:00'))


def test_parse_performer_misplaced():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            PERFORMER "3 Doors Down"
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0] == Error(Line(4, '    PERFORMER "3 Doors Down"'))


def test_parse_remark():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        REM foo bar
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert len(cue_sheet.remarks) == 1
    assert cue_sheet.remarks[0].remark == 'foo bar'
    assert not cue_sheet.errors


def test_parse_remark_in_file():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            REM foo bar
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert not cue_sheet.remarks
    assert cue_sheet.file and cue_sheet.file.remarks
    assert cue_sheet.file.remarks[0].remark == 'foo bar'
    assert not cue_sheet.errors


def test_parse_remark_in_track():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TRACK 01 AUDIO
                REM foo bar
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert not cue_sheet.remarks
    assert cue_sheet.file and not cue_sheet.file.remarks
    assert cue_sheet.file.tracks and cue_sheet.file.tracks[0].remarks
    assert cue_sheet.file.tracks[0].remarks[0].remark == 'foo bar'
    assert not cue_sheet.errors


def test_parse_title_misplaced():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TITLE "Away From The Sun"
        FILE "album.wav" WAVE
            TITLE "Away From The Sun"
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet and cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'

    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0] == Error(
        Line(4, '    TITLE "Away From The Sun"')
    )


def test_parse_track_misplaced():
    source = make_test_data("""
        PERFORMER "3 Doors Down"
        TRACK 01 AUDIO
        TITLE "Away From The Sun"
    """)
    cue_sheet = CueSheet.parse(source)
    assert cue_sheet
    assert len(cue_sheet.errors) == 1
    assert cue_sheet.errors[0] == Error(Line(2, 'TRACK 01 AUDIO'))


def read_test_data(filename: str) -> str:
    path = TEST_DATA_DIR / filename
    return path.read_text()


def make_test_data(s: str) -> str:
    return dedent(s).lstrip()


def parse_str(cue_sheet_str: str) -> CueSheet2:
    dedented = dedent(cue_sheet_str).lstrip()
    lexer = Lexer(StringIO(dedented))
    parser = Parser(lexer.lex())
    builder = Builder(parser.parse())
    return builder.build_cue_sheet()
