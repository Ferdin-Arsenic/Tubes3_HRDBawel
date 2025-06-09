import PyQt6.QtWidgets as QWidgets
import PyQt6.QtCore as QtCore



class PillButton(QWidgets.QRadioButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; padding: 5px;")
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

class AlgorithmButtons(QWidgets.QWidget):
    CHOICES = [
        "KMP", "BM", "Aho-Corasick"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.group = QWidgets.QButtonGroup(self)
        self.group.setExclusive(True)

        self.layout = QWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        
        
        for id, choice in enumerate(AlgorithmButtons.CHOICES):
            button = PillButton(choice, self)
            self.group.addButton(button, id)
            self.layout.addWidget(button)
            if id == 0:
                button.setChecked(True)
        
        self.group.idClicked.connect(self.on_choice_changed)

    def on_choice_changed(self, buttonId):
        print("Selected algorithm:", AlgorithmButtons.CHOICES[buttonId])

    def get_selected_algorithm(self) -> str:
        return AlgorithmButtons.CHOICES[self.group.checkedId()]