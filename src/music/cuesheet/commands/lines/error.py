from __future__ import annotations

from dataclasses import dataclass

from .line import Line


@dataclass
class Error(Line):
    @classmethod
    def from_line(cls, line: Line) -> Error:
        return cls(line.line_number, line.line)
