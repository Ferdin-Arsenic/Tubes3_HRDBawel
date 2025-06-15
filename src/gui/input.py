from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QSpinBox
from PyQt6.QtCore import pyqtSignal, Qt
from gui.algorithm_choice import AlgorithmButtons
from models.search import SearchParams

class InputFields(QWidget):
    search_initiate = pyqtSignal(SearchParams)   # Search button signal

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("color: #000000;")

        container = QVBoxLayout(self)
        container.setContentsMargins(20, 5, 20, 5)
        container.setSpacing(10)

        self.initialize_widgets(container)
    
    def initialize_widgets(self, layout) -> None:
        font_size = 14
        font_family = "Inter, sans-serif"
        normal_text_style = f"font-size: {font_size}px; font-weight: bold; font-family: {font_family}; padding: 0px; margin: 0px;"

        app_title = QLabel("Applicant Search")
        app_title.setStyleSheet("font-size: 24px; font-weight: bold; font-family: Inter, sans-serif;")
        layout.addWidget(app_title)

        keywords_label = QLabel(text="Keywords:")
        keywords_label.setStyleSheet(normal_text_style)
        layout.addWidget(keywords_label)

        self.keywords_input = QTextEdit()
        self.keywords_input.setPlaceholderText("Enter keywords separated by commas")
        self.keywords_input.setStyleSheet(normal_text_style + "background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px; padding: 5px; font-weight: normal;")
        font_metrics = self.keywords_input.fontMetrics()
        vertical_padding = 20
        self.keywords_input.setMaximumHeight(vertical_padding + font_metrics.lineSpacing() * 2)  # Limit to 2 lines
        layout.addWidget(self.keywords_input)

        algorithm_label = QLabel(text="Search Algorithm")
        algorithm_label.setStyleSheet(normal_text_style)
        layout.addWidget(algorithm_label)

        self.algorithm_choice = AlgorithmButtons()
        layout.addWidget(self.algorithm_choice)

        top_matches_layout = QHBoxLayout()
        top_matches_layout.setContentsMargins(0, 0, 0, 0)
        top_matches_layout.setSpacing(10)
        layout.addLayout(top_matches_layout)
        top_matches_label = QLabel(text="Top Matches:")
        top_matches_label.setStyleSheet(normal_text_style)
        top_matches_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_matches_layout.addWidget(top_matches_label)

        self.top_matches_input = QSpinBox()
        self.top_matches_input.setRange(1, 100)
        self.top_matches_input.setValue(10)
        self.top_matches_input.setFixedWidth(30)
        self.top_matches_input.setSingleStep(1)
        self.top_matches_input.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                font-family: Inter, sans-serif;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            /* This is the key part: it hides the button area completely */
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                border: none;
            }
        """)
        self.top_matches_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.top_matches_input.setMaximumWidth(100)
        top_matches_layout.addWidget(self.top_matches_input)
        top_matches_layout.addStretch(1)

        layout.addSpacing(20)
        search_button = QPushButton(text="Search", clicked=self.on_search_clicked)
        search_button.setMinimumHeight(40)
        search_button.setStyleSheet(normal_text_style + "background-color: #657E51; color: #ffffff; border: none; border-radius: 10px; font-size: 20px;")
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(search_button)

        layout.addStretch(1)

    def on_search_clicked(self) -> None:
        input = self.get_input()
        self.search_initiate.emit(input)

    def get_input(self) -> SearchParams:
        return SearchParams(
            self.keywords_input.toPlainText().strip().split(","),
            self.algorithm_choice.get_selected_algorithm(),
            self.top_matches_input.value()
        )