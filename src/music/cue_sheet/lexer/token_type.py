from enum import auto, Enum


class TokenType(Enum):
    EOL = auto()
    IDX_PT = auto()
    INT = auto()
    NAME = auto()
    QSTR = auto()
    STR = auto()
    WS = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


EOL = TokenType.EOL
IDX_PT = TokenType.IDX_PT
INT = TokenType.INT
NAME = TokenType.NAME
QSTR = TokenType.QSTR
STR = TokenType.STR
WS = TokenType.WS
