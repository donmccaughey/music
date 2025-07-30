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

        self.artists = []
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

        self.box_layout = QVBoxLayout(self)

        self.title = QLabel('-- ♫ Music ♫ --')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont('Arial', 24))
        self.box_layout.addWidget(self.title)

        self.artists_list = QListWidget()
        for artist in self.artists:
            item = QListWidgetItem(artist.name)
            self.artists_list.addItem(item)
        # TODO: can the list widget sort itself?
        self.box_layout.addWidget(self.artists_list)

        self.status_bar = QLabel(
            f'{len(self.artists)} artists'
        )
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box_layout.addWidget(self.status_bar)


def run_app(root: Path, paths: list[Path], verbose: bool):
    app = QApplication([])

    main_window = MainWindow(root, paths, verbose)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
