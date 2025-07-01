from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from .command import Command
from .lines import Line
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

        return cls(line.line_number, line.line, remark)
