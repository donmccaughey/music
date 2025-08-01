from PySide6.QtWidgets import QWidget, QHBoxLayout

from music.library.library import Library

from .albums_list import AlbumsList
from .artists_list import ArtistsList


class MainWindow(QWidget):
    def __init__(self, library: Library):
        super().__init__()

        self.library = library

        self.setWindowTitle('Music')
        h_box_layout = QHBoxLayout(self)

        self.artists_list = ArtistsList()
        h_box_layout.addWidget(self.artists_list.group_box)
        self.artists_list.list_widget.currentItemChanged.connect(
            self.update_albumns_list
        )
        self.artists_list.show_artists(self.library.artists)

        self.albums_list = AlbumsList()
        h_box_layout.addWidget(self.albums_list.group_box)

    def update_albumns_list(self, current, previous):
        if current:
            name = current.text()
            artist = self.library.artists_by_name[name]
            self.albums_list.show_albums(artist.albums)
        else:
            self.albums_list.show_albums([])
