from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout

from music.library.library import Library

from .album_list import AlbumList
from .artist_list import ArtistList
from .track_list import TrackList


class MainWindow(QWidget):
    def __init__(self, library: Library):
        super().__init__()

        self.library = library

        self.setWindowTitle('Music')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 10)
        layout.setSpacing(8)

        self.artist_list = ArtistList()
        layout.addWidget(self.artist_list.group_box)
        self.artist_list.list_widget.currentItemChanged.connect(
            self.change_artist
        )

        self.album_list = AlbumList()
        layout.addWidget(self.album_list.group_box)
        self.album_list.list_widget.currentItemChanged.connect(
            self.change_album
        )

        self.track_list = TrackList()
        layout.addWidget(self.track_list.group_box)

        self.artist_list.set_models(self.library.artists)

    @Slot()
    def change_artist(self, current, previous):
        if current:
            artist_name = current.text()
            artist = self.library.get_artist(artist_name)
            assert artist
            self.album_list.set_models(artist.albums)
        else:
            self.album_list.set_models([])

    @Slot()
    def change_album(self, current, previous):
        if current:
            artist_name = self.artist_list.list_widget.currentItem().text()
            album_title = current.text()
            album = self.library.get_album(artist_name, album_title)
            assert album
            self.track_list.set_models(album.tracks)
        else:
            self.track_list.set_models([])
