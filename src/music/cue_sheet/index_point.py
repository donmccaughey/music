from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IndexPoint:
    minutes: int
    seconds: int
    frames: int

    def __str__(self) -> str:
        return f'{self.minutes:02d}:{self.seconds:02d}:{self.frames:02d}'

    @classmethod
    def parse(cls, text: str) -> IndexPoint | None:
        if (
            8 == len(text)
            and text[0:2].isdigit()
            and text[2] == ':'
            and text[3:5].isdigit()
            and text[5] == ':'
            and text[6:8].isdigit()
        ):
            mm = int(text[0:2])
            ss = int(text[3:5])
            ff = int(text[6:8])
            return cls(mm, ss, ff)
        else:
            return None
