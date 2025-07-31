from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QGroupBox,
)

from .library import Library


class ArtistsList:
    def __init__(self, library: Library):
        self.library = library

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

        self.status_bar = QLabel(f'{len(self.library.artists)} artists')
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box_layout.addWidget(self.status_bar)

        for artist in self.library.artists:
            item = QListWidgetItem(artist.name)
            # TODO: can I attach an Artist object to the item?
            self.list_widget.addItem(item)
        # TODO: can the list widget sort itself?
