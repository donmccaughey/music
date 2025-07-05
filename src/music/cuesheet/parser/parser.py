from __future__ import annotations

from typing import Iterator

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .error import Error
from .file import File
from .index import Index
from .node import Node
from .performer import Performer
from .root import Root
from .title import Title
from .track import Track


class Parser:
    def __init__(self, tokens: Iterator[Token]):
        self.root = Root([], [])
        self.tokens = [token for token in tokens if TokenType.WS != token.type]
        self.end = len(self.tokens)
        self.i = 0
        self.stack: list[Node] = [self.root]

    @property
    def parent(self) -> Node:
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
            assert self.peek_token
            if TokenType.NAME == self.peek_token.type:
                self.command()
            elif TokenType.EOL == self.peek_token.type:
                self.next_token()
            else:
                self.error()
        return self.root

    def command(self):
        assert self.peek_token
        if 'FILE' == self.peek_token.value:
            self.file()
        elif 'INDEX' == self.peek_token.value:
            self.index()
        elif 'PERFORMER' == self.peek_token.value:
            self.performer()
        elif 'TITLE' == self.peek_token.value:
            self.title()
        elif 'TRACK' == self.peek_token.value:
            self.track()
        else:
            self.error()

    def error(self):
        error = Error([], [])
        self.parent.children.append(error)
        while token := self.next_token():
            error.tokens.append(token)
            if TokenType.EOL == token.type:
                return

    def file(self):
        tokens = self.peek_tokens(4)
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.QSTR,
            TokenType.NAME,
            TokenType.EOL,
        ] == types and tokens[2].value in ['WAVE']:
            if isinstance(self.parent, File):
                self.stack.pop()
            file = File(tokens=tokens[1:-1], children=[])
            self.parent.children.append(file)
            self.stack.append(file)
            self.next_token(4)
        else:
            self.error()

    def index(self):
        tokens = self.peek_tokens(4)
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.INT,
            TokenType.IDX_PT,
            TokenType.EOL,
        ] == types:
            index = Index(tokens=tokens[1:-1], children=[])
            self.parent.children.append(index)
            self.next_token(4)
        else:
            self.error()

    def performer(self):
        tokens = self.peek_tokens(3)
        types = [t.type for t in tokens]
        if [TokenType.NAME, TokenType.QSTR, TokenType.EOL] == types:
            self.parent.children.append(Performer(tokens[1:-1], []))
            self.next_token(3)
        else:
            self.error()

    def title(self):
        tokens = self.peek_tokens(3)
        types = [t.type for t in tokens]
        if [TokenType.NAME, TokenType.QSTR, TokenType.EOL] == types:
            self.parent.children.append(Title(tokens[1:-1], []))
            self.next_token(3)
        else:
            self.error()

    def track(self):
        tokens = self.peek_tokens(4)
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.INT,
            TokenType.NAME,
            TokenType.EOL,
        ] == types and tokens[2].value in ['AUDIO']:
            if isinstance(self.parent, Track):
                self.stack.pop()
            track = Track(tokens=tokens[1:-1], children=[])
            self.parent.children.append(track)
            self.stack.append(track)
            self.next_token(4)
        else:
            self.error()
