from dataclasses import dataclass
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


@dataclass
class Album:
    title: str


@dataclass
class Artist:
    name: str
    albums: list[Album]


class MainWindow(QWidget):
    def __init__(self, root: Path, paths: list[Path], verbose: bool):
        super().__init__()

        self.root = root
        self.paths = paths
        self.verbose = verbose

        self.artists: list[Artist] = []
        self.artists_by_name: dict[str, Artist] = {}

        for path in self.paths:
            relative_path = path.relative_to(root)
            artist_name, album_title, _ = relative_path.parts
            if not self.artists or artist_name != self.artists[-1].name:
                # TODO: sort albums
                artist = Artist(name=artist_name, albums=[])
                self.artists.append(artist)
                self.artists_by_name[artist_name] = artist
            album = Album(album_title)
            self.artists[-1].albums.append(album)
        # TODO: sort albums of last artist
        self.artists.sort(key=lambda a: a.name)

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

        self.status_bar = QLabel(f'{len(self.artists)} artists')
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

        for artist in self.artists:
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
        artist = self.artists_by_name[name]
        for album in artist.albums:
            item = QListWidgetItem(album.title)
            self.albums_list.addItem(item)
        self.albums_status_bar.setText(f'{len(artist.albums)} albums')
