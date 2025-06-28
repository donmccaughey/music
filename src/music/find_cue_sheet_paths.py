from pathlib import Path


def find_cue_sheet_paths(root: Path) -> list[Path]:
    paths = list(root.rglob('cuesheet*.txt'))
    paths.sort()
    return paths
