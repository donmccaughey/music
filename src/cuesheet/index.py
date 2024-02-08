from dataclasses import dataclass


@dataclass
class Index:
    minutes: int
    seconds: int
    frames: int

    @staticmethod
    def parse(index: str) -> tuple[int, 'Index'] | None:
        parts = [part for part in index.split() if part]
        if len(parts) != 3:
            return None
        if parts[0].upper() != 'INDEX':
            return None
        # todo remove zero padding
        i = int(parts[1])
        hours, minutes, frames = [int(time) for time in parts[2].split(':')]
        return (
            i,
            Index(hours, minutes, frames)
        )
