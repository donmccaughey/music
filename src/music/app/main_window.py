from PySide6.QtWidgets import QWidget, QHBoxLayout

from music.library.library import Library

from .albums_list import AlbumsList
from .artists_list import ArtistsList
from .tracks_list import TracksList


class MainWindow(QWidget):
    def __init__(self, library: Library):
        super().__init__()

        self.library = library

        self.setWindowTitle('Music')
        h_box_layout = QHBoxLayout(self)

        self.artists_list = ArtistsList()
        h_box_layout.addWidget(self.artists_list.group_box)
        self.artists_list.list_widget.currentItemChanged.connect(
            self.update_albums_list
        )
        self.artists_list.show_artists(self.library.artists)

        self.albums_list = AlbumsList()
        h_box_layout.addWidget(self.albums_list.group_box)
        self.albums_list.list_widget.currentItemChanged.connect(
            self.update_tracks_list
        )

        self.tracks_list = TracksList()
        h_box_layout.addWidget(self.tracks_list.group_box)

    def update_albums_list(self, current, previous):
        if current:
            artist_name = current.text()
            artist = self.library.get_artist(artist_name)
            assert artist
            self.albums_list.show_albums(artist.albums)
        else:
            self.albums_list.show_albums([])

    def update_tracks_list(self, current, previous):
        if current:
            artist_name = self.artists_list.list_widget.currentItem().text()
            album_title = current.text()
            album = self.library.get_album(artist_name, album_title)
            assert album
            self.tracks_list.show_tracks(album.tracks)
        else:
            self.tracks_list.show_tracks([])
