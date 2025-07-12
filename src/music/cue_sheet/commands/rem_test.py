import pytest

from music.cue_sheet.lexer.line import Line

from .rem import Rem


@pytest.mark.parametrize(
    'rem_string, expected_remark',
    [
        ('REM Something', 'Something'),
        ('REM Something, something!', 'Something, something!'),
        ('  REM \t   Something,  something!  ', 'Something, something!'),
    ],
)
def test_rem_parse(rem_string, expected_remark):
    rem = Rem.parse(Line(42, rem_string))
    assert rem
    assert rem.line == Line(42, rem_string)
    assert rem.remark == expected_remark


@pytest.mark.parametrize(
    'rem_string',
    [
        'REM: Something',
        'RM Mice',
        'Cat',
        '   ',
        '',
    ],
)
def test_rem_parse_fails(rem_string):
    rem = Rem.parse(Line(42, rem_string))
    assert not rem
