from io import StringIO
from pathlib import Path

from music import find_cue_sheet_paths
from music import parse_options
from music import write_report


def test_find_cue_sheet_paths():
    root = Path(__file__).parent / 'cuesheet/test_data'
    paths = find_cue_sheet_paths(root)
    assert paths
    assert len(paths) == 3


def test_parse_options():
    options = parse_options(['mypath'])
    assert isinstance(options.root, Path)
    assert options.root == Path('mypath')


def test_write_report():
    root = Path(__file__).parent / 'cuesheet/test_data'
    paths = find_cue_sheet_paths(root)
    sio = StringIO()

    write_report(root, paths, sio, True)

    lines = [line for line in sio.getvalue().splitlines()]

    assert len(lines) == 6
    assert lines == [
        'Found 3 cue sheets in ' + str(root),
        '    - cuesheet.txt',
        '    - double_album/cuesheet1.txt',
        '    - double_album/cuesheet2.txt',
        '- Unicode errors in 0 files',
        '- Parsing errors in 0 files',
    ]
