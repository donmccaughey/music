from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IndexPoint:
    minutes: int
    seconds: int
    frames: int
