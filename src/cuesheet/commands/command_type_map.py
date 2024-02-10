from .command import CommandType
from .file import File
from .index import Index
from .performer import Performer
from .title import Title
from .track import Track

command_types: list[CommandType] = [
    File,
    Index,
    Performer,
    Title,
    Track,
]

command_type_map: dict[str, CommandType] = {
    command_type.__name__.upper(): command_type
    for command_type in command_types
}
