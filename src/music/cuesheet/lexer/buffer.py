class Buffer:
    def __init__(self, n: int, line: str):
        self.n = n
        self.line = line

        self.start = self.i = 0
        self.end = len(line)

    @property
    def at_end(self) -> bool:
        return self.i == self.end

    @property
    def at_start(self) -> bool:
        return self.start == self.i

    @property
    def ch(self) -> str:
        return self.line[self.i]

    @property
    def has_more(self) -> bool:
        return self.i < self.end

    @property
    def has_text(self) -> bool:
        return self.start < self.i

    @property
    def text(self) -> str:
        return self.line[self.start : self.i]

    def next_ch(self):
        self.i += 1

    def start_next(self):
        self.start = self.i
