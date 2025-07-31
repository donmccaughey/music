from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QHBoxLayout,
)

from .library import Library
from .artists_list import ArtistsList


class MainWindow(QWidget):
    def __init__(self, library: Library):
        super().__init__()
        self.library = library

        self.setWindowTitle('Music')

        self.box_layout = QVBoxLayout(self)

        horizontal_layout = QHBoxLayout()
        self.box_layout.addLayout(horizontal_layout)

        # artists
        self.artists_list = ArtistsList(self.library)
        horizontal_layout.addWidget(self.artists_list.group_box)
        self.artists_list.list_widget.currentItemChanged.connect(
            self.update_albumns_list
        )

        # albums

        albums_group = QGroupBox()
        albumns_layout = QVBoxLayout(albums_group)
        albumns_layout.setContentsMargins(1, 2, 1, 2)
        albumns_layout.setSpacing(2)
        horizontal_layout.addWidget(albums_group)

        albumns_title = QLabel('Albums')
        albumns_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        albumns_layout.addWidget(albumns_title)

        self.albums_list = QListWidget()
        self.albums_list.setFont(QFont('Arial', 14))
        albumns_layout.addWidget(self.albums_list)

        self.albums_status_bar = QLabel('No albums')
        self.albums_status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        albumns_layout.addWidget(self.albums_status_bar)

        # populate artists

        for artist in self.library.artists:
            item = QListWidgetItem(artist.name)
            # TODO: can I attach an Artist object to the item?
            self.artists_list.list_widget.addItem(item)
        # TODO: can the list widget sort itself?

    def update_albumns_list(self, current, previous):
        self.albums_list.clear()
        if not current:
            self.albums_status_bar.setText('No albums')
            return

        name = current.text()
        artist = self.library.artists_by_name[name]
        for album in artist.albums:
            item = QListWidgetItem(album.title)
            self.albums_list.addItem(item)
        self.albums_status_bar.setText(f'{len(artist.albums)} albums')
