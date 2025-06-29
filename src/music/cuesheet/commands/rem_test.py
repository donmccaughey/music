import pytest

from .rem import Rem


@pytest.mark.parametrize(
    'rem_string, expected_remark',
    [
        ('REM Something', 'Something'),
        ('REM Something, something!', 'Something, something!'),
        ('  REM \t   Something,  something!  ', 'Something, something!'),
    ]
)
def test_rem_parse(rem_string, expected_remark):
    rem = Rem.parse(42, rem_string)
    assert rem
    assert rem.line_number == 42
    assert rem.line == rem_string
    assert rem.remark == expected_remark


@pytest.mark.parametrize('rem_string', [
    'REM: Something',
    'RM Mice',
    'Cat',
    '   ',
    '',
])
def test_performer_parse_fails(rem_string):
    rem = Rem.parse(42, rem_string)
    assert not rem
