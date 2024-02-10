from dataclasses import dataclass

from .line import Line


@dataclass
class Error(Line):
    pass
