from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSpinBox
from PyQt6.QtCore import pyqtSignal, Qt
from gui.algorithm_choice import AlgorithmButtons

class InputFields(QWidget):
    search_initiate = pyqtSignal(dict)   # Search button signal

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("color: #000000;")

        self.container = QVBoxLayout(self)
        self.container.setContentsMargins(5, 5, 5, 5)
        self.container.setSpacing(0)

        self.initialize_widgets()
    
    def initialize_widgets(self) -> None:
        font_size = 14
        font_family = "Inter, sans-serif"
        normal_text_style = f"font-size: {font_size}px; font-family: {font_family}; padding: 0px; margin: 0px;"

        app_title = QLabel("Applicant Search")
        app_title.setStyleSheet("font-size: 24px; font-weight: bold; font-family: Inter, sans-serif;")
        self.container.addWidget(app_title)

        keywords_label = QLabel(text="Keywords:")
        keywords_label.setStyleSheet(normal_text_style)
        self.container.addWidget(keywords_label)

        self.keywords_input = QTextEdit()
        self.keywords_input.setPlaceholderText("Enter keywords separated by commas")
        self.keywords_input.setStyleSheet(normal_text_style + "background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        font_metrics = self.keywords_input.fontMetrics()
        vertical_padding = 20
        self.keywords_input.setMaximumHeight(vertical_padding + font_metrics.lineSpacing() * 2)  # Limit to 2 lines
        self.container.addWidget(self.keywords_input)

        algorithm_label = QLabel(text="Search Algorithm")
        algorithm_label.setStyleSheet(normal_text_style)
        self.container.addWidget(algorithm_label)

        self.algorithm_choice = AlgorithmButtons()
        self.container.addWidget(self.algorithm_choice)

        top_matches_label = QLabel(text="Top Matches:")
        top_matches_label.setStyleSheet(normal_text_style)
        self.container.addWidget(top_matches_label)

        self.top_matches_input = QSpinBox()
        self.top_matches_input.setRange(1, 100)
        self.top_matches_input.setValue(10)
        self.top_matches_input.setStyleSheet(normal_text_style)
        self.container.addWidget(self.top_matches_input)

        search_button = QPushButton(text="Search", clicked=self.on_search_clicked)
        search_button.setStyleSheet(normal_text_style)
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.container.addWidget(search_button)

    def on_search_clicked(self) -> None:
        input = self.get_input()
        self.search_initiate.emit(input)

    def get_input(self) -> dict:
        return {
            "keywords": self.keywords_input.toPlainText().strip().split(","),
            "algorithm": self.algorithm_choice.get_selected_algorithm(),
            "top_matches": self.top_matches_input.value()
        }