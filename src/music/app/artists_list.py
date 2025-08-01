from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QGroupBox,
)

from music.library import Library, Artist


class ArtistsList:
    def __init__(self):
        self.group_box = QGroupBox()

        v_box_layout = QVBoxLayout(self.group_box)
        v_box_layout.setContentsMargins(1, 2, 1, 2)
        v_box_layout.setSpacing(2)

        title = QLabel('Artists')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box_layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont('Arial', 14))
        v_box_layout.addWidget(self.list_widget)

        self.status_bar = QLabel('No artists')
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box_layout.addWidget(self.status_bar)

    def show_artists(self, artists: list[Artist]):
        self.list_widget.clear()
        sorted_artists = sorted(artists, key=lambda artist: artist.name)

        for artist in sorted_artists:
            item = QListWidgetItem(artist.name)
            self.list_widget.addItem(item)

        self.status_bar.setText(
            f'{len(artists)} artists' if artists else 'No artists'
        )
