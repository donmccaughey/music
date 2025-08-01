from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QGroupBox,
)

from music.library import Album


class AlbumsList:
    def __init__(self):
        self.group_box = QGroupBox()

        v_box_layout = QVBoxLayout(self.group_box)
        v_box_layout.setContentsMargins(1, 2, 1, 2)
        v_box_layout.setSpacing(2)

        title = QLabel('Albums')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box_layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont('Arial', 14))
        v_box_layout.addWidget(self.list_widget)

        self.status_bar = QLabel('No albums')
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box_layout.addWidget(self.status_bar)

    def show_albums(self, albums: list[Album]):
        self.list_widget.clear()

        if albums:
            for album in albums:
                item = QListWidgetItem(album.title)
                self.list_widget.addItem(item)
            self.status_bar.setText(f'{len(albums)} albums')
        else:
            self.status_bar.setText('No albums')
