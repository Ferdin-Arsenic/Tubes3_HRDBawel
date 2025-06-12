from PyQt6.QtWidgets import QWidget, QHBoxLayout, QButtonGroup, QRadioButton
from PyQt6.QtCore import Qt
from models.search import SearchAlgorithm

class PillButton(QRadioButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; padding: 5px;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class AlgorithmButtons(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        
        
        for id, choice in enumerate(SearchAlgorithm):
            button = PillButton(choice.value, self)
            self.group.addButton(button, id)
            self.layout.addWidget(button)
            if id == 0:
                button.setChecked(True)
        
        self.group.idClicked.connect(self.on_choice_changed)

    def on_choice_changed(self, buttonId) -> None:
        # print("Selected algorithm:", AlgorithmButtons.CHOICES[buttonId])
        pass

    def get_selected_algorithm(self) -> SearchAlgorithm:
        for button in self.group.buttons():
            if button.isChecked():
                return SearchAlgorithm(button.text())