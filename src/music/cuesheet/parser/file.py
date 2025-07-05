from dataclasses import dataclass

from .command import Command
from .parent import Parent


@dataclass
class File(Command, Parent):
    pass
