from __future__ import annotations

from dataclasses import dataclass

from .split import split_tokens
from .command import Command


@dataclass
class Rem(Command):
    remark: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Rem | None:
        tokens = split_tokens(line)
        if not tokens:
            return None

        if tokens[0].upper() != 'REM':
            return None

        remark = ' '.join(tokens[1:])

        return cls(line_number, line, remark)
