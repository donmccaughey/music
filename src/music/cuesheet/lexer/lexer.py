from typing import TextIO, Generator

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


LWS = '\t '


class Lexer:
    commands: dict[str, type[Command]] = {
        'FILE': File,
        'INDEX': Index,
        'PERFORMER': Performer,
        'REM': Rem,
        'TITLE': Title,
        'TRACK': Track,
    }

    def __init__(self, source: TextIO):
        self.source = source

    def lex(self) -> Generator[Token]:
        n = 1
        for line in self.source:
            yield from self._lex_line(n, line)
            n += 1

    def _lex_line(self, n: int, line: str) -> Generator[Token]:
        buf = Buffer(line)
        scanning = TokenType.WS
        while buf.has_more:
            if scanning == TokenType.EOL:
                assert '\n' == buf.ch
                buf.next_ch()
                assert buf.at_end
                yield Token.make(n, TokenType.EOL, buf.token)
                buf.start_token()

            elif scanning == TokenType.IDX_PT:
                if buf.ch.isdigit():
                    buf.next_ch()
                elif ':' == buf.ch:
                    buf.next_ch()
                elif '\n' == buf.ch:
                    yield Token.make(n, TokenType.IDX_PT, buf.token)
                    scanning = TokenType.EOL
                    buf.start_token()
                elif buf.ch in LWS:
                    yield Token.make(n, TokenType.IDX_PT, buf.token)
                    scanning = TokenType.WS
                    buf.start_token()
                else:
                    scanning = TokenType.STR
                    buf.next_ch()

            elif scanning == TokenType.INT:
                if buf.ch.isdigit():
                    buf.next_ch()
                elif ':' == buf.ch:
                    scanning = TokenType.IDX_PT
                    buf.next_ch()
                elif '\n' == buf.ch:
                    yield Token.make(n, TokenType.INT, buf.token)
                    scanning = TokenType.EOL
                    buf.start_token()
                elif buf.ch in LWS:
                    yield Token.make(n, TokenType.INT, buf.token)
                    scanning = TokenType.WS
                    buf.start_token()
                else:
                    scanning = TokenType.STR
                    buf.next_ch()

            elif scanning == TokenType.NAME:
                if buf.ch.isalpha():
                    buf.next_ch()
                elif '\n' == buf.ch:
                    yield Token.make(n, TokenType.NAME, buf.token)
                    scanning = TokenType.EOL
                    buf.start_token()
                elif buf.ch in LWS:
                    yield Token.make(n, TokenType.NAME, buf.token)
                    scanning = TokenType.WS
                    buf.start_token()
                else:
                    scanning = TokenType.STR
                    buf.next_ch()

            elif scanning == TokenType.QSTR:
                if '"' == buf.ch:
                    if buf.at_token_start:
                        buf.next_ch()
                    else:
                        buf.next_ch()
                        yield Token.make(n, TokenType.QSTR, buf.token)
                        scanning = TokenType.WS
                        buf.start_token()
                elif '\n' == buf.ch:
                    yield Token.make(n, TokenType.STR, buf.token)
                    scanning = TokenType.EOL
                    buf.start_token()
                else:
                    buf.next_ch()

            elif scanning == TokenType.WS:
                if buf.ch in LWS:
                    buf.next_ch()
                elif buf.ch.isalpha():
                    if buf.has_token:
                        yield Token.make(n, TokenType.WS, buf.token)
                    scanning = TokenType.NAME
                    buf.start_token()
                elif buf.ch.isdigit():
                    if buf.has_token:
                        yield Token.make(n, TokenType.WS, buf.token)
                    scanning = TokenType.INT
                    buf.start_token()
                elif '"' == buf.ch:
                    if buf.has_token:
                        yield Token.make(n, TokenType.WS, buf.token)
                    scanning = TokenType.QSTR
                    buf.start_token()
                elif '\n' == buf.ch:
                    if buf.has_token:
                        yield Token.make(n, TokenType.WS, buf.token)
                    scanning = TokenType.EOL
                    buf.start_token()
                else:
                    if buf.has_token:
                        yield Token.make(n, TokenType.WS, buf.token)
                    scanning = TokenType.STR
                    buf.start_token()

            else:
                raise RuntimeError(f'Unexpected lexer state: {scanning}')

        if buf.has_token:
            if scanning == TokenType.QSTR:
                yield Token.make(n, TokenType.STR, buf.token)
            else:
                yield Token.make(n, scanning, buf.token)

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
