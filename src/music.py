import argparse
import sys

from pathlib import Path
from typing import TextIO

from cuesheet import CueSheet


def parse_options(args: list[str] | None = None) -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description='Finds and check cue sheets')
    argument_parser.add_argument('root', metavar='ROOT', type=Path,
                                 help='Root directory to search for cue sheets')
    return argument_parser.parse_args(args if args else sys.argv)


def find_cue_sheet_paths(root: Path) -> list[Path]:
    return list(root.rglob('cuesheet*.txt'))


def write_report(root: Path, paths: list[Path], out: TextIO):
    out.write(f'Found {len(paths)} cue sheets in {root}\n')
    for path in paths:
        s = path.read_text()
        cue_sheet = CueSheet.parse(s)
        relative_path = path.relative_to(root)
        out.write(f'- {relative_path}:\n')
        if cue_sheet.errors:
            for error in cue_sheet.errors:
                out.write(f'    + {error.line_number}: {error.line}\n')
        else:
            out.write(f'    okay\n')


def main():
    options = parse_options()
    paths = find_cue_sheet_paths(options.root)
    write_report(options.root, paths, sys.stdout)


if __name__ == '__main__':
    main()
