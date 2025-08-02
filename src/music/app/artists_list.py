from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QGroupBox,
)

from music.library import Artist


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

        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_status_bar(0)
        v_box_layout.addWidget(self.status_bar)

    def set_artists(self, artists: list[Artist]):
        self.list_widget.setCurrentRow(-1)
        self.list_widget.clear()

        if artists:
            sorted_artists = sorted(artists, key=lambda artist: artist.name)
            for artist in sorted_artists:
                item = QListWidgetItem(artist.name)
                self.list_widget.addItem(item)
            self.list_widget.setCurrentRow(0)

        self.set_status_bar(len(artists))

    def set_status_bar(self, count: int):
        amount = str(count) if count else 'No'
        label = 'artist' if 1 == count else 'artists'
        self.status_bar.setText(f'{amount} {label}')
