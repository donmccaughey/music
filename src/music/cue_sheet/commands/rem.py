from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from music.cue_sheet.lexer.line import Line

from .command import Command
from .split import split_tokens


@dataclass
class Rem(Command):
    remark: str

    @classmethod
    def parse(cls, line: Line) -> Self | None:
        tokens = split_tokens(line.line)
        if not tokens:
            return None

        if tokens[0].upper() != 'REM':
            return None

        remark = ' '.join(tokens[1:])

        return cls(line, remark)
