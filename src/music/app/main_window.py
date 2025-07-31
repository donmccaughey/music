from PySide6.QtWidgets import (
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from .albums_list import AlbumsList
from .artists_list import ArtistsList
from .library import Library


class MainWindow(QWidget):
    def __init__(self, library: Library):
        super().__init__()
        self.library = library

        self.setWindowTitle('Music')
        h_box_layout = QHBoxLayout(self)

        self.artists_list = ArtistsList(self.library)
        h_box_layout.addWidget(self.artists_list.group_box)
        self.artists_list.list_widget.currentItemChanged.connect(
            self.update_albumns_list
        )

        self.albums_list = AlbumsList()
        h_box_layout.addWidget(self.albums_list.group_box)

        # populate artists

        for artist in self.library.artists:
            item = QListWidgetItem(artist.name)
            # TODO: can I attach an Artist object to the item?
            self.artists_list.list_widget.addItem(item)
        # TODO: can the list widget sort itself?

    def update_albumns_list(self, current, previous):
        self.albums_list.list_widget.clear()
        if not current:
            self.albums_list.status_bar.setText('No albums')
            return

        name = current.text()
        artist = self.library.artists_by_name[name]
        for album in artist.albums:
            item = QListWidgetItem(album.title)
            self.albums_list.list_widget.addItem(item)
        self.albums_list.status_bar.setText(f'{len(artist.albums)} albums')
