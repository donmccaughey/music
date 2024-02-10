from typing import Type
from typing import TypeVar

from .field import Field
from .file import File
from .index import Index
from .performer import Performer
from .title import Title

F = TypeVar('F', bound=Field)

FieldType = Type[F]

types: list[FieldType] = [
    File,
    Index,
    Performer,
    Title,
]

type_map: dict[str, FieldType] = {
    field_type.__name__.upper(): field_type for field_type in types
}
