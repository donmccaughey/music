from dataclasses import dataclass

from music.cuesheet import IndexPoint

from .token_type import TokenType


@dataclass(frozen=True, slots=True)
class Token:
    line: int
    type: TokenType
    value: str | int | IndexPoint
