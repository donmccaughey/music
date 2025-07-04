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

from .buffer import Buffer
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
            yield from self._lex_line(n, line)
            n += 1

    def _lex_line(self, n: int, line: str) -> Generator[Token]:
        buf = Buffer(n, line)
        scanning = TokenType.WS
        while buf.has_more:
            if scanning == TokenType.EOL:
                assert '\n' == buf.ch
                buf.next_ch()
                assert buf.at_end
                yield Token(buf.n, TokenType.EOL, buf.text)
                buf.start_next()

            elif scanning == TokenType.IDX_PT:
                if buf.ch.isdigit() or ':' == buf.ch:
                    buf.next_ch()
                elif buf.ch.isspace():
                    text = buf.text
                    if index_point := IndexPoint.parse(text):
                        yield Token(n, TokenType.IDX_PT, index_point)
                    else:
                        yield Token(n, TokenType.STR, text)
                    scanning = TokenType.EOL if '\n' == buf.ch else TokenType.WS
                    buf.start_next()
                else:
                    scanning = TokenType.STR
                    buf.next_ch()

            elif scanning == TokenType.INT:
                if buf.ch.isdigit():
                    buf.next_ch()
                elif ':' == buf.ch:
                    scanning = TokenType.IDX_PT
                    buf.next_ch()
                elif buf.ch.isspace():
                    if buf.has_text:
                        yield Token(n, TokenType.INT, int(buf.text))
                    scanning = TokenType.EOL if '\n' == buf.ch else TokenType.WS
                    buf.start_next()
                else:
                    scanning = TokenType.STR
                    buf.next_ch()

            elif scanning == TokenType.NAME:
                if buf.ch.isalpha():
                    buf.next_ch()
                elif buf.ch.isspace():
                    if buf.has_text:
                        text = buf.text
                        token_type = (
                            TokenType.NAME
                            if text in self.names
                            else TokenType.STR
                        )
                        yield Token(n, token_type, text)
                    scanning = TokenType.EOL if '\n' == buf.ch else TokenType.WS
                    buf.start_next()
                else:
                    scanning = TokenType.STR
                    buf.next_ch()

            elif scanning == TokenType.QSTR:
                if '"' == buf.ch:
                    if buf.at_start:
                        buf.next_ch()
                    else:
                        buf.next_ch()
                        yield Token(n, TokenType.QSTR, buf.text.strip('"'))
                        scanning = TokenType.WS
                        buf.start_next()
                elif '\n' == buf.ch:
                    yield Token(n, TokenType.STR, buf.text)
                    scanning = TokenType.EOL
                    buf.start_next()
                else:
                    buf.next_ch()

            elif scanning == TokenType.WS:
                if buf.ch.isspace() and '\n' != buf.ch:
                    buf.next_ch()
                else:
                    if buf.has_text:
                        yield Token(n, TokenType.WS, buf.text)

                    if buf.ch.isalpha():
                        scanning = TokenType.NAME
                    elif buf.ch.isdigit():
                        scanning = TokenType.INT
                    elif '"' == buf.ch:
                        scanning = TokenType.QSTR
                    elif '\n' == buf.ch:
                        scanning = TokenType.EOL
                    else:
                        scanning = TokenType.STR
                    buf.start_next()

            else:
                raise RuntimeError(f'Unexpected lexer state: {scanning}')
        if buf.has_text:
            text = buf.text
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
