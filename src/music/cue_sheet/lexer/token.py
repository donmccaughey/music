from dataclasses import dataclass
from typing import Self

from music.cue_sheet import IndexPoint

from .token_type import EOL, IDX_PT, INT, NAME, QSTR, STR, TokenType, WS


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
        return self.type == EOL

    @property
    def is_whitespace(self) -> bool:
        return self.type == WS

    @classmethod
    def make(cls, n: int, token_type: TokenType, text: str) -> Self:
        if IDX_PT == token_type:
            if index_point := IndexPoint.parse(text):
                return cls(n, IDX_PT, index_point)
            else:
                return cls(n, STR, text)

        elif INT == token_type:
            return cls(n, INT, int(text))

        elif NAME == token_type:
            if text in NAMES:
                return cls(n, NAME, text)
            else:
                return cls(n, STR, text)

        elif QSTR == token_type:
            return cls(n, QSTR, text.strip('"'))

        else:
            return cls(n, token_type, text)
