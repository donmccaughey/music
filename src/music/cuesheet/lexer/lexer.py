from typing import TextIO, Generator

from music.cuesheet import IndexPoint
from music.cuesheet.commands import (
    Blank,
    Command,
    Error,
    File,
    Index,
    Performer,
    Rem,
    split_tokens,
    Title,
    Track,
)

from .line import Line
from .token import Token
from .token_type import TokenType


class Lexer:
    commands: dict[str, type[Command]] = {
        'FILE': File,
        'INDEX': Index,
        'PERFORMER': Performer,
        'REM': Rem,
        'TITLE': Title,
        'TRACK': Track,
    }

    names = [
        'AUDIO',
        'FILE',
        'INDEX',
        'PERFORMER',
        'REM',
        'TITLE',
        'TRACK',
        'WAVE',
    ]

    def __init__(self, source: TextIO):
        self.source = source

    def lex(self) -> Generator[Token]:
        n = 1
        for line in self.source:
            start = i = 0
            end = len(line)
            scanning = TokenType.WS
            while i < end:
                ch = line[i]

                if scanning == TokenType.EOL:
                    assert '\n' == ch
                    i += 1
                    assert i == end
                    yield Token(n, TokenType.EOL, line[start:i])
                    start = i

                elif scanning == TokenType.IDX_PT:
                    if ch.isdigit() or ':' == ch:
                        i += 1
                    elif ch.isspace():
                        text = line[start:i]
                        if index_point := IndexPoint.parse(text):
                            yield Token(n, TokenType.IDX_PT, index_point)
                        else:
                            yield Token(n, TokenType.STR, text)
                        scanning = TokenType.EOL if '\n' == ch else TokenType.WS
                        start = i
                    else:
                        scanning = TokenType.STR
                        i += 1

                elif scanning == TokenType.INT:
                    if ch.isdigit():
                        i += 1
                    elif ':' == ch:
                        scanning = TokenType.IDX_PT
                        i += 1
                    elif ch.isspace():
                        if start < i:
                            yield Token(n, TokenType.INT, int(line[start:i]))
                        scanning = TokenType.EOL if '\n' == ch else TokenType.WS
                        start = i
                    else:
                        scanning = TokenType.STR
                        i += 1

                elif scanning == TokenType.NAME:
                    if ch.isalpha():
                        i += 1
                    elif ch.isspace():
                        if start < i:
                            text = line[start:i]
                            token_type = (
                                TokenType.NAME
                                if text in self.names
                                else TokenType.STR
                            )
                            yield Token(n, token_type, text)
                        scanning = TokenType.EOL if '\n' == ch else TokenType.WS
                        start = i
                    else:
                        scanning = TokenType.STR
                        i += 1

                elif scanning == TokenType.QSTR:
                    if '"' == ch:
                        if i == start:
                            i += 1
                        else:
                            i += 1
                            yield Token(
                                n, TokenType.QSTR, line[start + 1 : i - 1]
                            )
                            scanning = TokenType.WS
                            start = i
                    elif '\n' == ch:
                        yield Token(n, TokenType.STR, line[start:i])
                        scanning = TokenType.EOL
                        start = i
                    else:
                        i += 1

                elif scanning == TokenType.WS:
                    if ch.isspace() and '\n' != ch:
                        i += 1
                    else:
                        if start < i:
                            yield Token(n, TokenType.WS, line[start:i])

                        if ch.isalpha():
                            scanning = TokenType.NAME
                        elif ch.isdigit():
                            scanning = TokenType.INT
                        elif '"' == ch:
                            scanning = TokenType.QSTR
                        elif '\n' == ch:
                            scanning = TokenType.EOL
                        else:
                            scanning = TokenType.STR
                        start = i

                else:
                    raise RuntimeError(f'Unexpected lexer state: {scanning}')
            if start < i:
                text = line[start:i]
                value: str | int | IndexPoint = text
                if scanning == TokenType.IDX_PT:
                    if index_point := IndexPoint.parse(text):
                        value = index_point
                    else:
                        scanning = TokenType.STR
                elif scanning == TokenType.INT:
                    value = int(text)
                elif scanning == TokenType.QSTR:
                    scanning = TokenType.STR
                yield Token(n, scanning, value)
            n += 1

    def scan(self) -> Generator[Command]:
        for i, line in enumerate(self.source):
            yield self.scan_line(i + 1, line.strip('\n'))

    def scan_line(self, line_number: int, line: str) -> Command:
        tokens = split_tokens(line)

        if not tokens:
            return Blank(Line(line_number, line))

        command_name = tokens[0]
        if command_name in self.commands:
            command_type = self.commands[command_name]
            command = command_type.parse(Line(line_number, line))
            return command if command else Error(Line(line_number, line))

        return Error(Line(line_number, line))
