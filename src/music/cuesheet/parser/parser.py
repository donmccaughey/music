from __future__ import annotations

from typing import Iterator

from music.cuesheet.lexer.token import Token
from music.cuesheet.lexer.token_type import TokenType

from .asin import ASIN
from .comment import Comment
from .disc_id import DiscID
from .error import Error
from .file import File
from .genre import Genre
from .index import Index
from .node import Node
from .performer import Performer
from .rem import Rem
from .root import Root
from .title import Title
from .track import Track
from .year import Year


class Parser:
    def __init__(self, tokens: Iterator[Token]):
        self.root = Root([])
        self.tokens = tokens
        self.stack: list[Node] = [self.root]

    @property
    def parent(self) -> Node:
        return self.stack[-1]

    def next_line(self) -> list[Token]:
        tokens = []
        while token := next(self.tokens, None):
            if TokenType.WS != token.type:
                tokens.append(token)
            if TokenType.EOL == token.type:
                break

        assert not tokens or TokenType.EOL == tokens[-1].type
        return tokens

    def parse(self) -> Root:
        while tokens := self.next_line():
            if TokenType.NAME == tokens[0].type:
                self.command(tokens)
            elif TokenType.EOL == tokens[0].type:
                pass
            else:
                self.error(tokens)
        return self.root

    def command(self, tokens: list[Token]):
        assert tokens
        if 'FILE' == tokens[0].value:
            self.file(tokens)
        elif 'INDEX' == tokens[0].value:
            self.index(tokens)
        elif 'PERFORMER' == tokens[0].value:
            self.performer(tokens)
        elif 'REM' == tokens[0].value:
            self.rem(tokens)
        elif 'TITLE' == tokens[0].value:
            self.title(tokens)
        elif 'TRACK' == tokens[0].value:
            self.track(tokens)
        else:
            self.error(tokens)

    def error(self, tokens: list[Token]) -> None:
        assert tokens
        error = Error(tokens[0].line_num)
        self.parent.children.append(error)

    def asin(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.NAME,
            TokenType.STR,
            TokenType.EOL,
        ] == types:
            self.parent.children.append(ASIN(tokens[2:-1]))
        else:
            self.error(tokens)

    def comment(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.NAME,
            TokenType.QSTR,
            TokenType.EOL,
        ] == types:
            self.parent.children.append(Comment(tokens[2:-1]))
        else:
            self.error(tokens)

    def disc_id(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.NAME,
            TokenType.STR,
            TokenType.EOL,
        ] == types:
            self.parent.children.append(DiscID(tokens[2:-1]))
        else:
            self.error(tokens)

    def file(self, tokens: list[Token]):
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
        else:
            self.error(tokens)

    def genre(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.NAME,
            TokenType.QSTR,
            TokenType.EOL,
        ] == types:
            self.parent.children.append(Genre(tokens[2:-1]))
        else:
            self.error(tokens)

    def index(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.INT,
            TokenType.IDX_PT,
            TokenType.EOL,
        ] == types:
            index = Index(tokens[1:-1])
            self.parent.children.append(index)
        else:
            self.error(tokens)

    def performer(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [TokenType.NAME, TokenType.QSTR, TokenType.EOL] == types:
            self.parent.children.append(Performer(tokens[1:-1]))
        else:
            self.error(tokens)

    def rem(self, tokens: list[Token]):
        if len(tokens) > 1:
            if 'ASIN' == tokens[1].value:
                self.asin(tokens)
                return
            elif 'COMMENT' == tokens[1].value:
                self.comment(tokens)
                return
            elif 'DISCID' == tokens[1].value:
                self.disc_id(tokens)
                return
            elif 'GENRE' == tokens[1].value:
                self.genre(tokens)
                return
            elif 'YEAR' == tokens[1].value:
                self.year(tokens)
                return
        rem = Rem(tokens[1:-1])
        self.parent.children.append(rem)

    def title(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [TokenType.NAME, TokenType.QSTR, TokenType.EOL] == types:
            self.parent.children.append(Title(tokens))
        else:
            self.error(tokens)

    def track(self, tokens: list[Token]):
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
        else:
            self.error(tokens)

    def year(self, tokens: list[Token]):
        types = [t.type for t in tokens]
        if [
            TokenType.NAME,
            TokenType.NAME,
            TokenType.INT,
            TokenType.EOL,
        ] == types:
            self.parent.children.append(Year(tokens[2:-1]))
        else:
            self.error(tokens)
