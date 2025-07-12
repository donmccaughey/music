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
        self.line_stack: list[list[Token]] = []
        self.stack: list[Node] = [self.root]

    @property
    def parent(self) -> Node:
        return self.stack[-1]

    def next_line(self) -> list[Token]:
        if self.line_stack:
            return self.line_stack.pop()

        tokens = []
        it = filter_out(lambda t: t.is_whitespace, self.token_iter)
        while token := next(it, None):
            tokens.append(token)
            if token.is_end_of_line:
                break

        assert not tokens or TokenType.EOL == tokens[-1].type
        return tokens

    def push_line(self, line: list[Token]):
        self.line_stack.append(line)

    def parse(self) -> Root:
        self._parse_root(self.root)
        return self.root

    def _parse_root(self, root: Root):
        while tokens := self.next_line():
            if is_blank_line(tokens):
                continue
            elif file := File.parse(tokens):
                root.children.append(file)
                self._parse_file(file)
            elif performer := Performer.parse(tokens):
                root.children.append(performer)
            elif title := Title.parse(tokens):
                root.children.append(title)

            # check REM subtypes before REM
            elif asin := ASIN.parse(tokens):
                root.children.append(asin)
            elif comment := Comment.parse(tokens):
                root.children.append(comment)
            elif disc_id := DiscID.parse(tokens):
                root.children.append(disc_id)
            elif genre := Genre.parse(tokens):
                root.children.append(genre)
            elif year := Year.parse(tokens):
                root.children.append(year)

            elif rem := Rem.parse(tokens):
                root.children.append(rem)

            else:
                root.children.append(Error.from_line(tokens))

    def _parse_file(self, file: File):
        while tokens := self.next_line():
            if is_blank_line(tokens):
                continue
            elif File.is_file(tokens):
                self.push_line(tokens)
                return
            elif track := Track.parse(tokens):
                file.children.append(track)
                self._parse_track(track)
            elif rem := Rem.parse(tokens):
                file.children.append(rem)
            else:
                file.children.append(Error.from_line(tokens))

    def _parse_track(self, track: Track):
        while tokens := self.next_line():
            if is_blank_line(tokens):
                continue
            elif index := Index.parse(tokens):
                track.children.append(index)
            elif performer := Performer.parse(tokens):
                track.children.append(performer)
            elif title := Title.parse(tokens):
                track.children.append(title)
            elif Track.is_track(tokens):
                self.push_line(tokens)
                return
            elif rem := Rem.parse(tokens):
                track.children.append(rem)
            else:
                track.children.append(Error.from_line(tokens))


def is_blank_line(tokens: list[Token]) -> bool:
    return 1 == len(tokens) and TokenType.EOL == tokens[0].type
