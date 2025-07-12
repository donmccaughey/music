from __future__ import annotations

from typing import Iterator

from music.cue_sheet.lexer.token import Token
from music.cue_sheet.lexer.tokens import take_non_blank_line

from .commands import (
    ASIN,
    Comment,
    DiscID,
    File,
    Genre,
    Index,
    Performer,
    Rem,
    Title,
    Track,
    Year,
)
from .error import Error
from .root import Root


class Parser:
    def __init__(self, token_iter: Iterator[Token]):
        self.token_iter = token_iter
        self.line_stack: list[list[Token]] = []

    def parse(self) -> Root:
        root = Root([])
        self._parse_root(root)
        return root

    def _next_line(self) -> list[Token]:
        if self.line_stack:
            return self.line_stack.pop()
        else:
            return take_non_blank_line(self.token_iter)

    def _push_line(self, line: list[Token]):
        self.line_stack.append(line)

    def _parse_root(self, root: Root):
        while tokens := self._next_line():
            if file := File.parse(tokens):
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
                root.children.append(Error(tokens))

    def _parse_file(self, file: File):
        while tokens := self._next_line():
            if File.is_file(tokens):
                self._push_line(tokens)
                return
            elif track := Track.parse(tokens):
                file.children.append(track)
                self._parse_track(track)
            elif rem := Rem.parse(tokens):
                file.children.append(rem)
            else:
                file.children.append(Error(tokens))

    def _parse_track(self, track: Track):
        while tokens := self._next_line():
            if index := Index.parse(tokens):
                track.children.append(index)
            elif performer := Performer.parse(tokens):
                track.children.append(performer)
            elif title := Title.parse(tokens):
                track.children.append(title)
            elif Track.is_track(tokens):
                self._push_line(tokens)
                return
            elif rem := Rem.parse(tokens):
                track.children.append(rem)
            else:
                track.children.append(Error(tokens))
