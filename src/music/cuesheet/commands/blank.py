from dataclasses import dataclass

from .command import Command


@dataclass
class Blank(Command):
    pass
