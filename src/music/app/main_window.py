from pathlib import Path
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


class MainWindow(QWidget):
    def __init__(self, root: Path, paths: list[Path], verbose: bool):
        super().__init__()

        self.root = root
        self.paths = paths
        self.verbose = verbose

        self.library = Library(self.root, paths)

        self.setWindowTitle('Music')

        self.box_layout = QVBoxLayout(self)

        horizontal_layout = QHBoxLayout()
        self.box_layout.addLayout(horizontal_layout)

        # artists

        artists_group = QGroupBox()
        artists_layout = QVBoxLayout(artists_group)
        artists_layout.setContentsMargins(1, 2, 1, 2)
        artists_layout.setSpacing(2)
        horizontal_layout.addWidget(artists_group)

        artists_title = QLabel('Artists')
        artists_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        artists_layout.addWidget(artists_title)

        self.artists_list = QListWidget()
        self.artists_list.setFont(QFont('Arial', 14))
        self.artists_list.currentItemChanged.connect(self.update_albumns_list)
        artists_layout.addWidget(self.artists_list)

        self.status_bar = QLabel(f'{len(self.library.artists)} artists')
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        artists_layout.addWidget(self.status_bar)

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
            self.artists_list.addItem(item)
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
