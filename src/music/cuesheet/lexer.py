from typing import TextIO, Generator

from .commands import (
    Blank,
    CommandType,
    Error,
    File,
    Index,
    Line,
    Performer,
    Rem,
    split_tokens,
    Title,
    Track,
)


class Lexer:
    commands: dict[str, CommandType] = {
        'FILE': File,
        'INDEX': Index,
        'PERFORMER': Performer,
        'REM': Rem,
        'TITLE': Title,
        'TRACK': Track,
    }

    def scan(self, source: TextIO) -> Generator[Line]:
        for i, line in enumerate(source):
            yield self.scan_line(i + 1, line.strip('\n'))

    def scan_line(self, line_number: int, line: str) -> Line:
        tokens = split_tokens(line)

        if not tokens:
            return Blank(line_number, line)

        command_name = tokens[0]
        if command_name in self.commands:
            command_type = self.commands[command_name]
            command = command_type.parse(line_number, line)
            return command if command else Error(line_number, line)

        return Error(line_number, line)
