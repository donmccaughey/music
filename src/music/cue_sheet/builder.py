from .cue_sheet import CueSheet
from .error import Error
from .file import File
from .parser import (
    ASIN,
    Comment,
    DiscID,
    Error as ErrorNode,
    File as FileNode,
    Genre,
    Index,
    Performer,
    Rem,
    Root,
    Title,
    Track as TrackNode,
    Year,
)
from .track import Track


class Builder:
    def __init__(self, root: Root):
        self.root = root

    def build_cue_sheet(self) -> CueSheet:
        cue_sheet = CueSheet()
        for child in self.root.children:
            match child:
                case ASIN() as asin_node:
                    cue_sheet.asin = asin_node.value
                case Comment() as comment_node:
                    cue_sheet.comment = comment_node.value
                case DiscID() as disc_id:
                    cue_sheet.disc_id = disc_id.value
                case ErrorNode() as error_node:
                    cue_sheet.errors.append(
                        Error(error_node.line_num, error_node.value)
                    )
                case FileNode() as file_node:
                    cue_sheet.file = self._build_file(file_node)
                case Genre() as genre_node:
                    cue_sheet.genre = genre_node.value
                case Performer() as performer_node:
                    cue_sheet.performer = performer_node.value
                case Rem() as rem_node:
                    cue_sheet.remarks.append(rem_node.value)
                case Title() as title_node:
                    cue_sheet.title = title_node.value
                case Year() as year_node:
                    cue_sheet.year = year_node.value
                case _:
                    raise RuntimeError(f'Unexpected node {child}')
        return cue_sheet

    def _build_file(self, file_node: FileNode) -> File:
        file = File(file_node.filename, file_node.type)
        for child in file_node.children:
            match child:
                case ErrorNode() as error_node:
                    file.errors.append(
                        Error(error_node.line_num, error_node.value)
                    )
                case Rem() as rem_node:
                    file.remarks.append(rem_node.value)
                case TrackNode() as track_node:
                    track = self._build_track(track_node)
                    file.tracks.append(track)
                case _:
                    raise RuntimeError(f'Unexpected node {child}')
        return file

    def _build_track(self, track_node: TrackNode) -> Track:
        track = Track(track_node.number, track_node.type)
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
