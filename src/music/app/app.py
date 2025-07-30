import sys

from dataclasses import dataclass
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
    QGroupBox,
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
        for path in self.paths:
            relative_path = path.relative_to(root)
            artist_name, album_title, _ = relative_path.parts
            if not self.artists or artist_name != self.artists[-1].name:
                # TODO: sort albums
                artist = Artist(name=artist_name, albums=[])
                self.artists.append(artist)
            album = Album(album_title)
            self.artists[-1].albums.append(album)
        # TODO: sort albums of last artist
        self.artists.sort(key=lambda a: a.name)

        self.setWindowTitle('Music')

        self.box_layout = QVBoxLayout(self)

        artists_group = QGroupBox()
        artists_layout = QVBoxLayout(artists_group)
        artists_layout.setContentsMargins(1, 2, 1, 2)
        artists_layout.setSpacing(2)
        self.box_layout.addWidget(artists_group)

        artists_title = QLabel('Artists')
        artists_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        artists_layout.addWidget(artists_title)

        self.artists_list = QListWidget()
        self.artists_list.setFont(QFont('Arial', 14))
        artists_layout.addWidget(self.artists_list)

        self.status_bar = QLabel(f'{len(self.artists)} artists')
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        artists_layout.addWidget(self.status_bar)

        for artist in self.artists:
            item = QListWidgetItem(artist.name)
            self.artists_list.addItem(item)
        # TODO: can the list widget sort itself?


def run_app(root: Path, paths: list[Path], verbose: bool):
    app = QApplication([])

    main_window = MainWindow(root, paths, verbose)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
