from enum import auto, Enum


class TokenType(Enum):
    EOL = auto()
    INDEX_PT = auto()
    INT = auto()
    NAME = auto()
    QSTR = auto()
    STR = auto()
    WS = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
