import sys

from PySide6.QtWidgets import QApplication, QMenuBar

from music.library import Library

from .main_window import MainWindow


class App(QApplication):
    def __init__(self, library: Library):
        super().__init__([])

        self.library = library

        self.setApplicationDisplayName('Music')
        self.setApplicationName('Music')
        self.setApplicationVersion('0.0.1')

        self.menu_bar = QMenuBar()
        self.menu_bar.setNativeMenuBar(True)

    def run(self):
        main_window = MainWindow(self.library)
        main_window.resize(800, 600)
        main_window.show()
        sys.exit(self.exec())
