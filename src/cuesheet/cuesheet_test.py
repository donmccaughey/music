from pathlib import Path

from .cuesheet import CueSheet


def test_cue_sheet_parse():
    cue_sheet = CueSheet.parse(CUE_SHEET1)
    assert cue_sheet
    assert cue_sheet.performer
    assert cue_sheet.performer.name == '3 Doors Down'
    assert cue_sheet.title
    assert cue_sheet.title.title == 'Away From The Sun'
    assert cue_sheet.file
    assert cue_sheet.file.filename == Path('album.wav')
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


CUE_SHEET1 = '''
PERFORMER "3 Doors Down"
TITLE "Away From The Sun"
REM YEAR 2002
REM GENRE "Alt. Rock"
REM ASIN B00006ZCFG
REM DISCID 9E0B010C
REM COMMENT "ExactAudioCopy v0.95b4"
FILE "album.wav" WAVE
  TRACK 01 AUDIO
    TITLE "When I'm Gone"
    PERFORMER "3 Doors Down"
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Away From The Sun"
    PERFORMER "3 Doors Down"
    INDEX 00 04:20:38
    INDEX 01 04:21:66
  TRACK 03 AUDIO
    TITLE "The Road I'm On"
    PERFORMER "3 Doors Down"
    INDEX 00 08:13:50
    INDEX 01 08:15:10
  TRACK 04 AUDIO
    TITLE "Ticket To Heaven"
    PERFORMER "3 Doors Down"
    INDEX 01 12:14:70
  TRACK 05 AUDIO
    TITLE "Running Out Of Days"
    PERFORMER "3 Doors Down"
    INDEX 01 15:42:35
  TRACK 06 AUDIO
    TITLE "Here Without You"
    PERFORMER "3 Doors Down"
    INDEX 01 19:13:43
  TRACK 07 AUDIO
    TITLE "I Feel You"
    PERFORMER "3 Doors Down"
    INDEX 01 23:12:10
  TRACK 08 AUDIO
    TITLE "Dangerous Game"
    PERFORMER "3 Doors Down"
    INDEX 01 27:19:35
  TRACK 09 AUDIO
    TITLE "Changes"
    PERFORMER "3 Doors Down"
    INDEX 01 30:55:40
  TRACK 10 AUDIO
    TITLE "Going Down In Flames"
    PERFORMER "3 Doors Down"
    INDEX 01 34:52:30
  TRACK 11 AUDIO
    TITLE "Sarah Yellin'"
    PERFORMER "3 Doors Down"
    INDEX 01 38:21:03
  TRACK 12 AUDIO
    TITLE "This Time"
    PERFORMER "3 Doors Down"
    INDEX 01 41:38:70
'''
