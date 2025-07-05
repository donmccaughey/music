from dataclasses import dataclass

from .node import Node


@dataclass
class Parent(Node):
    children: list[Node]
