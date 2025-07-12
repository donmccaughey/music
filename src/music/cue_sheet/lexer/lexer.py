from typing import Generator, TextIO

from .buffer import Buffer
from .token import Token
from .token_type import EOL, IDX_PT, INT, NAME, QSTR, STR, TokenType, WS


LWS = '\t '


class Lexer:
    def __init__(self, source: TextIO):
        self.source = source

    def lex(self) -> Generator[Token]:
        n = 1
        for line in self.source:
            yield from self._lex_line(n, line)
            n += 1

    def _lex_line(self, n: int, line: str) -> Generator[Token]:
        buf = Buffer(line)
        scanning = WS
        while buf.has_more:
            if scanning == EOL:
                assert '\n' == buf.ch
                buf.next_ch()
                assert buf.at_end
                yield self._next_token(n, EOL, buf)

            elif scanning == IDX_PT:
                if buf.ch.isdigit():
                    buf.next_ch()
                elif ':' == buf.ch:
                    buf.next_ch()
                elif '\n' == buf.ch:
                    yield self._next_token(n, IDX_PT, buf)
                    scanning = EOL
                elif buf.ch in LWS:
                    yield self._next_token(n, IDX_PT, buf)
                    scanning = WS
                else:
                    scanning = STR
                    buf.next_ch()

            elif scanning == INT:
                if buf.ch.isdigit():
                    buf.next_ch()
                elif ':' == buf.ch:
                    scanning = IDX_PT
                    buf.next_ch()
                elif '\n' == buf.ch:
                    yield self._next_token(n, INT, buf)
                    scanning = EOL
                elif buf.ch in LWS:
                    yield self._next_token(n, INT, buf)
                    scanning = WS
                else:
                    scanning = STR
                    buf.next_ch()

            elif scanning == NAME:
                if buf.ch.isalpha():
                    buf.next_ch()
                elif '\n' == buf.ch:
                    yield self._next_token(n, NAME, buf)
                    scanning = EOL
                elif buf.ch in LWS:
                    yield self._next_token(n, NAME, buf)
                    scanning = WS
                else:
                    scanning = STR
                    buf.next_ch()

            elif scanning == STR:
                if '\n' == buf.ch:
                    yield self._next_token(n, NAME, buf)
                    scanning = EOL
                elif buf.ch in LWS:
                    yield self._next_token(n, NAME, buf)
                    scanning = WS
                else:
                    buf.next_ch()

            elif scanning == QSTR:
                if '"' == buf.ch:
                    if buf.at_token_start:
                        buf.next_ch()
                    else:
                        buf.next_ch()
                        yield self._next_token(n, QSTR, buf)
                        scanning = WS
                elif '\n' == buf.ch:
                    yield self._next_token(n, STR, buf)
                    scanning = EOL
                else:
                    buf.next_ch()

            elif scanning == WS:
                if buf.ch in LWS:
                    buf.next_ch()
                elif buf.ch.isalpha():
                    if buf.has_token:
                        yield self._next_token(n, WS, buf)
                    scanning = NAME
                elif buf.ch.isdigit():
                    if buf.has_token:
                        yield self._next_token(n, WS, buf)
                    scanning = INT
                elif '"' == buf.ch:
                    if buf.has_token:
                        yield self._next_token(n, WS, buf)
                    scanning = QSTR
                elif '\n' == buf.ch:
                    if buf.has_token:
                        yield self._next_token(n, WS, buf)
                    scanning = EOL
                else:
                    if buf.has_token:
                        yield self._next_token(n, WS, buf)
                    scanning = STR

            else:
                raise RuntimeError(f'Unexpected lexer state: {scanning}')

        if buf.has_token:
            if scanning == QSTR:
                yield Token.make(n, STR, buf.token)
            else:
                yield Token.make(n, scanning, buf.token)

    def _next_token(self, n: int, token_type: TokenType, buf: Buffer) -> Token:
        token = Token.make(n, token_type, buf.token)
        buf.start_token()
        return token
