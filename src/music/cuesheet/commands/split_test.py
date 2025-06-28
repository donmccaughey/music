from .split import split_ints, split_quoted_string, split_tokens


def test_split_quoted_string():
    assert split_quoted_string('TITLE', '') is None
    assert split_quoted_string('TITLE', 'REM "The Title"') is None
    assert split_quoted_string('TITLE', 'TITLE 42') is None
    assert split_quoted_string('TITLE', 'TITLE "42"') == '42'
    assert split_quoted_string('TITLE', 'TITLE "The Title"') == 'The Title'
    assert split_quoted_string(
        'TITLE', 'TITLE "The  Messy \t Title"'
    ) == 'The Messy Title'


def test_split_ints():
    assert split_ints('', ':') == []
    assert split_ints('01-23-45', ':') == []
    assert split_ints('01:23:45', ':') == [1, 23, 45]
    assert split_ints('09:12:34', ':') == [9, 12, 34]


def test_split_tokens():
    assert split_tokens('') == []
    assert split_tokens('REM 42') == ['REM', '42']
    assert split_tokens('TITLE \t "The Title"') == ['TITLE', '"The', 'Title"']
