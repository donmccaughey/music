import sys

from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.box_layout = QVBoxLayout(self)

        self.text = QLabel('-- ♫ Music ♫ --')
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text.setFont(QFont('Arial', 24))
        self.box_layout.addWidget(self.text)


def run_app(root: Path, paths: list[Path], verbose: bool):
    app = QApplication([])

    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
