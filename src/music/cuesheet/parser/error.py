from dataclasses import dataclass

from .node import Node


@dataclass
class Error(Node):
    pass
