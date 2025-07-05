from __future__ import annotations

from typing import Iterator

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .error import Error
from .parent import Parent
from .performer import Performer
from .root import Root


class Parser:
    def __init__(self, tokens: Iterator[Token]):
        self.root = Root([])
        self.tokens = [token for token in tokens if TokenType.WS != token.type]
        self.end = len(self.tokens)
        self.i = 0
        self.stack: list[Parent] = [self.root]

    @property
    def parent(self) -> Parent:
        return self.stack[-1]

    @property
    def peek_token(self) -> Token | None:
        return self.tokens[self.i] if self.i < self.end else None

    def peek_tokens(self, count: int) -> list[Token]:
        tokens = []
        for i in range(self.i, self.i + count):
            if i < self.end:
                tokens.append(self.tokens[i])
        return tokens

    def next_token(self, step: int = 1) -> Token | None:
        if self.i < self.end:
            token = self.tokens[self.i]
            self.i += step
            return token
        else:
            return None

    def parse(self) -> Root:
        while self.peek_token:
            self.command()
        return self.root

    def command(self):
        assert self.peek_token
        if TokenType.NAME == self.peek_token.type:
            self.name()
        else:
            self.error()

    def error(self):
        error = Error([])
        self.parent.children.append(error)
        while token := self.next_token():
            error.tokens.append(token)
            if TokenType.EOL == token.type:
                return

    def name(self):
        assert self.peek_token
        if 'PERFORMER' == self.peek_token.value:
            self.performer()
        else:
            self.error()

    def performer(self):
        tokens = self.peek_tokens(3)
        types = [t.type for t in tokens]
        if [TokenType.NAME, TokenType.QSTR, TokenType.EOL] == types:
            self.parent.children.append(Performer(tokens))
            self.next_token(3)
        else:
            self.error()
