from dataclasses import dataclass
from typing import Self

from music.cue_sheet.lexer.line import Line


@dataclass
class Command:
    line: Line

    @classmethod
    def parse(cls, line: Line) -> Self | None:
        raise NotImplementedError()
