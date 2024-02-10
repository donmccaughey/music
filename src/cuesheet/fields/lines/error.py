from dataclasses import dataclass

from .line import Line


@dataclass
class Error(Line):
    @staticmethod
    def from_line(line: Line) -> 'Error':
        return Error(line.line_number, line.line)
