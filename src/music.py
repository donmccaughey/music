import argparse
import sys

from pathlib import Path
from typing import TextIO

from cuesheet import CueSheet


def parse_options(args: list[str] | None = None) -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description='Finds and check cue sheets')
    argument_parser.add_argument('root', metavar='ROOT', type=Path,
                                 help='Root directory to search for cue sheets')
    return argument_parser.parse_args(args if args else sys.argv[1:])


def find_cue_sheet_paths(root: Path) -> list[Path]:
    paths = list(root.rglob('**/cuesheet*.txt'))
    paths.sort()
    return paths


def write_report(root: Path, paths: list[Path], out: TextIO):
    out.write(f'Found {len(paths)} cue sheets in {root}\n')
    for path in paths:
        relative_path = path.relative_to(root)
        out.write(f'- {relative_path}:\n')

        try:
            s = path.read_text()
            cue_sheet = CueSheet.parse(s)

            if cue_sheet.errors:
                for error in cue_sheet.errors:
                    out.write(f'    + {error.line_number}: {error.line}\n')
        except UnicodeDecodeError as e:
            out.write(f'    + {e}\n')


def main():
    options = parse_options()
    root = options.root.expanduser()
    paths = find_cue_sheet_paths(root)
    write_report(root, paths, sys.stdout)


if __name__ == '__main__':
    main()
