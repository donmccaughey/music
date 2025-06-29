from __future__ import annotations

import sys

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Options:
    root: Path
    verbose: bool

    @classmethod
    def parse(cls, args: list[str] | None = None) -> Options:
        parser = ArgumentParser(description='Finds and check cue sheets')
        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='List correctly parsed cue sheets and errors',
        )
        parser.add_argument(
            'root',
            help='Root directory to search for cue sheets',
            metavar='ROOT',
            type=Path,
        )
        namespace = parser.parse_args(args if args else sys.argv[1:])
        return cls(root=namespace.root, verbose=namespace.verbose)
