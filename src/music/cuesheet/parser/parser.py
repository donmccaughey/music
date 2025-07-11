from __future__ import annotations

from itertools import filterfalse as filter_out
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
    def __init__(self, token_iter: Iterator[Token]):
        self.root = Root([])
        self.token_iter = token_iter
        self.stack: list[Node] = [self.root]

    @property
    def parent(self) -> Node:
        return self.stack[-1]

    def next_line(self) -> list[Token]:
        tokens = []
        it = filter_out(lambda t: t.is_whitespace, self.token_iter)
        while token := next(it, None):
            tokens.append(token)
            if token.is_end_of_line:
                break

        assert not tokens or TokenType.EOL == tokens[-1].type
        return tokens

    def parse(self) -> Root:
        while tokens := self.next_line():
            if is_command(tokens):
                self.command(tokens)
            elif is_blank_line(tokens):
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
        if asin := ASIN.parse(tokens):
            self.parent.children.append(asin)
        else:
            self.error(tokens)

    def comment(self, tokens: list[Token]):
        if comment := Comment.parse(tokens):
            self.parent.children.append(comment)
        else:
            self.error(tokens)

    def disc_id(self, tokens: list[Token]):
        if disc_id := DiscID.parse(tokens):
            self.parent.children.append(disc_id)
        else:
            self.error(tokens)

    def file(self, tokens: list[Token]):
        if file := File.parse(tokens):
            if isinstance(self.parent, File):
                self.stack.pop()
            self.parent.children.append(file)
            self.stack.append(file)
        else:
            self.error(tokens)

    def genre(self, tokens: list[Token]):
        if genre := Genre.parse(tokens):
            self.parent.children.append(genre)
        else:
            self.error(tokens)

    def index(self, tokens: list[Token]):
        if index := Index.parse(tokens):
            self.parent.children.append(index)
        else:
            self.error(tokens)

    def performer(self, tokens: list[Token]):
        if performer := Performer.parse(tokens):
            self.parent.children.append(performer)
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
        if rem := Rem.parse(tokens):
            self.parent.children.append(rem)
        else:
            self.error(tokens)

    def title(self, tokens: list[Token]):
        if title := Title.parse(tokens):
            self.parent.children.append(title)
        else:
            self.error(tokens)

    def track(self, tokens: list[Token]):
        if track := Track.parse(tokens):
            if isinstance(self.parent, Track):
                self.stack.pop()
            self.parent.children.append(track)
            self.stack.append(track)
        else:
            self.error(tokens)

    def year(self, tokens: list[Token]):
        if year := Year.parse(tokens):
            self.parent.children.append(year)
        else:
            self.error(tokens)


def is_command(tokens: list[Token]) -> bool:
    return len(tokens) > 1 and TokenType.NAME == tokens[0].type


def is_blank_line(tokens: list[Token]) -> bool:
    return 1 == len(tokens) and TokenType.EOL == tokens[0].type
