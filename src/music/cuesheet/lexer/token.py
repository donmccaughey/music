from dataclasses import dataclass
from typing import Self

from music.cuesheet import IndexPoint

from .token_type import TokenType


NAMES = [
    'ASIN',
    'AUDIO',
    'COMMENT',
    'DISCID',
    'FILE',
    'GENRE',
    'INDEX',
    'PERFORMER',
    'REM',
    'TITLE',
    'TRACK',
    'WAVE',
    'YEAR',
]


@dataclass(frozen=True, slots=True)
class Token:
    line_num: int
    type: TokenType
    value: str | int | IndexPoint

    @property
    def is_end_of_line(self) -> bool:
        return self.type == TokenType.EOL

    @property
    def is_whitespace(self) -> bool:
        return self.type == TokenType.WS

    @classmethod
    def make(cls, n: int, token_type: TokenType, text: str) -> Self:
        if TokenType.IDX_PT == token_type:
            if index_point := IndexPoint.parse(text):
                return cls(n, TokenType.IDX_PT, index_point)
            else:
                return cls(n, TokenType.STR, text)

        elif TokenType.INT == token_type:
            return cls(n, TokenType.INT, int(text))

        elif TokenType.NAME == token_type:
            if text in NAMES:
                return cls(n, TokenType.NAME, text)
            else:
                return cls(n, TokenType.STR, text)

        elif TokenType.QSTR == token_type:
            return cls(n, TokenType.QSTR, text.strip('"'))

        else:
            return cls(n, token_type, text)
