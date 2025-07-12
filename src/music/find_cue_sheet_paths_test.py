from pathlib import Path

from .find_cue_sheet_paths import find_cue_sheet_paths


def test_find_cue_sheet_paths():
    root = Path(__file__).parent / 'cue_sheet/test_data'
    paths = find_cue_sheet_paths(root)
    assert paths
    assert len(paths) == 3
