from .cuesheet import CueSheet2, Error2, File2, Track2

from .parser import (
    ASIN,
    Comment,
    DiscID,
    Error,
    File,
    Genre,
    Index,
    Performer,
    Rem,
    Root,
    Title,
    Track,
    Year,
)


class Builder:
    def __init__(self, root: Root):
        self.root = root

    def build_cue_sheet(self) -> CueSheet2:
        cue_sheet = CueSheet2()
        for child in self.root.children:
            match child:
                case ASIN() as asin_node:
                    cue_sheet.asin = asin_node.value
                case Comment() as comment_node:
                    cue_sheet.comment = comment_node.value
                case DiscID() as disc_id:
                    cue_sheet.disc_id = disc_id.value
                case Error() as error_node:
                    cue_sheet.errors.append(
                        Error2(error_node.line_num, error_node.value)
                    )
                case File() as file_node:
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
