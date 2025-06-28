import argparse
import sys

from pathlib import Path


def parse_options(args: list[str] | None = None) -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description='Finds and check cue sheets')
    argument_parser.add_argument('-v', '--verbose', action='store_true',
                                 help='List correctly parsed cue sheets and errors')
    argument_parser.add_argument('root', metavar='ROOT', type=Path,
                                 help='Root directory to search for cue sheets')
    return argument_parser.parse_args(args if args else sys.argv[1:])
