import PyQt6.QtWidgets as QWidgets
import PyQt6.QtCore as QtCore
from gui.algorithm_choice import AlgorithmButtons

class InputFields(QWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("color: #000000;")

        self.container = QWidgets.QVBoxLayout(self)
        self.container.setContentsMargins(5, 5, 5, 5)
        self.container.setSpacing(0)

        self.initialize_widgets()
    
    def initialize_widgets(self):
        font_size = 14
        font_family = "Inter, sans-serif"
        normal_text_style = f"font-size: {font_size}px; font-family: {font_family}; padding: 0px; margin: 0px;"

        self.app_title = QWidgets.QLabel("Applicant Search")
        self.app_title.setStyleSheet("font-size: 24px; font-weight: bold; font-family: Inter, sans-serif;")
        self.container.addWidget(self.app_title)

        self.keywords_label = QWidgets.QLabel(text="Keywords:")
        self.keywords_label.setStyleSheet(normal_text_style)

        self.container.addWidget(self.keywords_label)

        self.keywords_input = QWidgets.QTextEdit()
        ## Settings here
        self.keywords_input.setPlaceholderText("Enter keywords separated by commas")
        self.keywords_input.setStyleSheet(normal_text_style + "background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        font_metrics = self.keywords_input.fontMetrics()
        vertical_padding = 20
        self.keywords_input.setMaximumHeight(vertical_padding + font_metrics.lineSpacing() * 2)  # Limit to 2 lines
        self.container.addWidget(self.keywords_input)

        self.algorithm_label = QWidgets.QLabel(text="Search Algorithm")
        self.algorithm_label.setStyleSheet(normal_text_style)
        self.container.addWidget(self.algorithm_label)

        self.algorithm_choice = AlgorithmButtons()
        self.container.addWidget(self.algorithm_choice)

        self.top_matches_label = QWidgets.QLabel(text="Top Matches:")
        self.top_matches_label.setStyleSheet(normal_text_style)
        self.container.addWidget(self.top_matches_label)

        self.top_matches_input = QWidgets.QSpinBox()
        self.top_matches_input.setRange(1, 100)
        self.top_matches_input.setValue(10)
        self.top_matches_input.setStyleSheet(normal_text_style)
        self.container.addWidget(self.top_matches_input)

        self.search_button = QWidgets.QPushButton(text="Search", clicked=self.on_search_clicked)
        self.search_button.setStyleSheet(normal_text_style)
        self.search_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.container.addWidget(self.search_button)


    def on_search_clicked(self):
        input = self.get_input()
        print("Search options:")
        for key, value in input.items():
            print(f"    {key}: {value}")

    def get_input(self) -> dict:
        return {
            "keywords": self.keywords_input.toPlainText().strip().split(","),
            "algorithm": self.algorithm_choice.get_selected_algorithm(),
            "top_matches": self.top_matches_input.value()
        }