from dataclasses import dataclass

from .line import Line


@dataclass
class Blank(Line):
    pass
