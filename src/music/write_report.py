from pathlib import Path
from typing import TextIO

from .cuesheet import CueSheet


def write_report(root: Path, paths: list[Path], out: TextIO, verbose: bool):
    good_cue_sheets: list[Path] = []
    unicode_errors: list[Path] = []
    parse_errors: list[tuple[Path, CueSheet]] = []
    for path in paths:
        relative_path = path.relative_to(root)

        try:
            s = path.read_text()
            cue_sheet = CueSheet.parse(s)

            if cue_sheet.errors:
                parse_errors.append((relative_path, cue_sheet))
            else:
                good_cue_sheets.append(relative_path)
        except UnicodeDecodeError as e:
            unicode_errors.append(relative_path)

    out.write(f'Found {len(paths)} cue sheets in {root}\n')
    if verbose:
        for path in good_cue_sheets:
            out.write(f'    - {path}\n')
    out.write(f'- Unicode errors in {len(unicode_errors)} files\n')
    if verbose:
        for path in unicode_errors:
            out.write(f'    - {path}\n')
    out.write(f'- Parsing errors in {len(parse_errors)} files\n')
    if verbose:
        for path, cue_sheet in parse_errors:
            out.write(f'    - {path}\n')
            for error in cue_sheet.errors:
                out.write(f'        - {error}\n')
