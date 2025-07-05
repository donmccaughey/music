from dataclasses import dataclass

from .command import Command


@dataclass
class Error(Command):
    pass
