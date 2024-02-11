from dataclasses import dataclass
from typing import Optional

from .split import split_tokens
from .command import Command


@dataclass
class Rem(Command):
    remark: str

    @classmethod
    def parse(cls, line_number: int, line: str) -> Optional['Rem']:
        tokens = split_tokens(line)
        if not tokens:
            return None

        if tokens[0].upper() != 'REM':
            return None

        remark = ' '.join(tokens[1:])

        return Rem(line_number, line, remark)
