import sys

from PySide6.QtWidgets import QApplication

from music.library import Library

from .main_window import MainWindow


def run_app(library: Library):
    app = QApplication([])

    main_window = MainWindow(library)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
