from io import StringIO
from pathlib import Path
from typing import TextIO

from .cuesheet.builder import Builder
from .cuesheet.cuesheet import CueSheet2
from .cuesheet.lexer.lexer import Lexer
from .cuesheet.parser.parser import Parser


def write_report(root: Path, paths: list[Path], out: TextIO, verbose: bool):
    good_cue_sheets: list[Path] = []
    unicode_errors: list[Path] = []
    parse_errors: list[tuple[Path, CueSheet2]] = []
    for path in paths:
        relative_path = path.relative_to(root)

        try:
            s = path.read_text()
            lexer = Lexer(StringIO(s))
            parser = Parser(lexer.lex())
            builder = Builder(parser.parse())
            cue_sheet = builder.build_cue_sheet()

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
