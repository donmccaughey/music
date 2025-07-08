from .cuesheet import CueSheet2, File2, Track2
from .parser.asin import ASIN
from .parser.comment import Comment
from .parser.disc_id import DiscID
from .parser.error import Error
from .parser.file import File
from .parser.genre import Genre
from .parser.index import Index
from .parser.performer import Performer
from .parser.rem import Rem
from .parser.root import Root
from .parser.title import Title
from .parser.track import Track
from .parser.year import Year


class Builder:
    def __init__(self, root: Root):
        self.root = root

    def build_cue_sheet(self) -> CueSheet2:
        cuesheet = CueSheet2()
        for child in self.root.children:
            match child:
                case ASIN() as asin_node:
                    cuesheet.asin = asin_node.value
                case Comment() as comment_node:
                    cuesheet.comment = comment_node.value
                case DiscID() as disc_id:
                    cuesheet.disc_id = disc_id.value
                case Error() as error_node:
                    cuesheet.errors.append(error_node.value)
                case File() as file_node:
                    cuesheet.file = self._build_file(file_node)
                case Genre() as genre_node:
                    cuesheet.genre = genre_node.value
                case Performer() as performer_node:
                    cuesheet.performer = performer_node.value
                case Rem() as rem_node:
                    cuesheet.remarks.append(rem_node.value)
                case Title() as title_node:
                    cuesheet.title = title_node.value
                case Year() as year_node:
                    cuesheet.year = year_node.value
                case _:
                    raise RuntimeError(f'Unexpected node {child}')
        return cuesheet

    def _build_file(self, file_node: File) -> File2:
        file = File2(file_node.filename, file_node.type)
        for child in file_node.children:
            match child:
                case Rem() as rem_node:
                    file.remarks.append(rem_node.value)
                case Track() as track_node:
                    track = self._build_track(track_node)
                    file.tracks.append(track)
                case _:
                    raise RuntimeError(f'Unexpected node {child}')
        return file

    def _build_track(self, track_node: Track) -> Track2:
        track = Track2(track_node.number, track_node.type)
        for child in track_node.children:
            match child:
                case Index() as index_node:
                    track.indices[index_node.number] = index_node.index_point
                case Performer() as performer_node:
                    track.performer = performer_node.value
                case Rem() as rem_node:
                    track.remarks.append(rem_node.value)
                case Title() as title_node:
                    track.title = title_node.value
                case _:
                    raise RuntimeError(f'Unexpected node {child}')
        return track
