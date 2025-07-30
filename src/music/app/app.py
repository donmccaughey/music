import sys

from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
    QTreeWidgetItem,
)


class MainWindow(QWidget):
    def __init__(self, root: Path, paths: list[Path], verbose: bool):
        super().__init__()

        self.root = root
        self.paths = paths
        self.verbose = verbose

        self.box_layout = QVBoxLayout(self)

        self.title = QLabel('-- ♫ Music ♫ --')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont('Arial', 24))
        self.box_layout.addWidget(self.title)

        self.paths_tree = QTreeWidget()
        self.paths_tree.setHeaderHidden(True)

        current_artist = ''
        artist_count = 0
        current_artist_item: QTreeWidgetItem | None = None

        current_album = ''
        album_count = 0

        for path in self.paths:
            relative_path = path.relative_to(root)
            artist, album, _ = relative_path.parts
            if artist != current_artist:
                current_artist = artist
                artist_count += 1
                current_artist_item = QTreeWidgetItem([artist])
                self.paths_tree.addTopLevelItem(current_artist_item)
            if album != current_album:
                current_album = album
                album_count += 1
                assert current_artist_item
                album_item = QTreeWidgetItem([album])
                current_artist_item.addChild(album_item)
        self.box_layout.addWidget(self.paths_tree)

        self.status_bar = QLabel(
            f'{album_count} albums from {artist_count} artists'
        )
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box_layout.addWidget(self.status_bar)


def run_app(root: Path, paths: list[Path], verbose: bool):
    app = QApplication([])

    main_window = MainWindow(root, paths, verbose)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
