import argparse
import sys

from pathlib import Path
from typing import TextIO

from cuesheet import CueSheet


def parse_options(args: list[str] | None = None) -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description='Finds and check cue sheets')
    argument_parser.add_argument('-v', '--verbose', action='store_true',
                                 help='List correctly parsed cue sheets and errors')
    argument_parser.add_argument('root', metavar='ROOT', type=Path,
                                 help='Root directory to search for cue sheets')
    return argument_parser.parse_args(args if args else sys.argv[1:])


def find_cue_sheet_paths(root: Path) -> list[Path]:
    paths = list(root.rglob('cuesheet*.txt'))
    paths.sort()
    return paths


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


def main():
    options = parse_options()
    root = options.root.expanduser()
    paths = find_cue_sheet_paths(root)
    write_report(root, paths, sys.stdout, options.verbose)


if __name__ == '__main__':
    main()
