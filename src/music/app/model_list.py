from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QGroupBox,
)


M = TypeVar('M')


class ModelList(Generic[M], ABC):
    def __init__(self, model_type: str):
        self.model_type = model_type

        self.group_box = QGroupBox()

        layout = QVBoxLayout(self.group_box)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(3)

        title = QLabel(self.model_type.title())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont('Arial', 14))
        layout.addWidget(self.list_widget)

        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_status_bar(0)
        layout.addWidget(self.status_bar)

    @abstractmethod
    def model_text(self, model: M) -> str: ...

    @abstractmethod
    def sort_models(self, models: list[M]) -> list[M]: ...

    def set_models(self, models: list[M]):
        self.list_widget.setCurrentRow(-1)
        self.list_widget.clear()

        if models:
            for model in self.sort_models(models):
                item = QListWidgetItem(self.model_text(model))
                self.list_widget.addItem(item)
            self.list_widget.setCurrentRow(0)

        self.set_status_bar(len(models))

    def set_status_bar(self, count: int):
        amount = str(count) if count else 'No'
        label = self.model_type if 1 == count else self.model_type + 's'
        self.status_bar.setText(f'{amount} {label}')
