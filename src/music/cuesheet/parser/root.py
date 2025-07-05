from dataclasses import dataclass

from .parent import Parent


@dataclass
class Root(Parent):
    pass
