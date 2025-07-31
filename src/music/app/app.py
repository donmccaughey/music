import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def run_app(root: Path, paths: list[Path], verbose: bool):
    app = QApplication([])

    main_window = MainWindow(root, paths, verbose)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
