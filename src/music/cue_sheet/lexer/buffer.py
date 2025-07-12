class Buffer:
    def __init__(self, chars: str):
        self.line = chars

        self.start = self.i = 0
        self.end = len(chars)

    @property
    def at_end(self) -> bool:
        return self.i == self.end

    @property
    def at_token_start(self) -> bool:
        return self.start == self.i

    @property
    def ch(self) -> str:
        return self.line[self.i]

    @property
    def has_more(self) -> bool:
        return self.i < self.end

    @property
    def has_token(self) -> bool:
        return self.start < self.i

    @property
    def token(self) -> str:
        return self.line[self.start : self.i]

    def next_ch(self):
        self.i += 1

    def start_token(self):
        self.start = self.i
