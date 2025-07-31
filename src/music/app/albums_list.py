from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QVBoxLayout,
    QGroupBox,
)


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
