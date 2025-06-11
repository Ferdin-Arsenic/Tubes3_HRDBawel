from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

class ResultDisplay(QWidget):
    """
        Grid 3x2 layout for displaying search results.
        The middle cell contains the search result cards, which have a grid layout of its own.
    """
    view_summary = pyqtSignal(int)  # Signal to view summary
    view_cv = pyqtSignal(int)       # Signal to view CV (launch a window with the CV PDF)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("color: #000000;")

        # Initialize widgets that is put into two layouts
        self.blank_layout = QVBoxLayout()
        self.container = QGridLayout()
        self.initialize_widgets()

        # Set pagination
        self.page_count = 0
        self.current_page = 0
        self.results_per_page = 4

        # Set the layout for blank state before anyy result is shown
        self.display_results()
        
    def initialize_widgets(self) -> None:
        self.blank_layout.setContentsMargins(5, 5, 5, 5)
        self.blank_layout.setSpacing(0)
        blank_label = QLabel("Search for applicants to see results here")
        blank_label.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; color: #444444;")
        blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blank_layout.addWidget(blank_label)

        # Container when a result is displayed
        self.container.setContentsMargins(5, 5, 5, 5)
        self.container.setSpacing(0)
        self.container.setRowMinimumHeight(1, 350)

        # Laying out the grid
        left_button = QPushButton("◀", clicked=self.on_prev_clicked)
        left_button.setStyleSheet("font-size: 25px;")
        left_button.setMaximumWidth(25)
        self.container.addWidget(left_button, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        right_button = QPushButton("▶", clicked=self.on_next_clicked)
        right_button.setStyleSheet("font-size: 25px;")
        right_button.setMaximumWidth(25)
        self.container.addWidget(right_button, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        result_card_layout = QGridLayout()
        result_card_layout.setContentsMargins(5, 5, 5, 5)
        result_card_layout.setSpacing(0)
        self.container.addLayout(result_card_layout, 1, 1)

        page_label = QLabel("0/0")
        page_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #444444;")
        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container.addWidget(page_label, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)

    def clear_results(self) -> None:
        self.setLayout(self.blank_layout)
    
    def display_results(self) -> None:
        self.setLayout(self.container)
    
    def set_results(self, results: dict) -> None:
        pass

    def on_prev_clicked(self) -> None:
        print("[Prev] Current page:", self.current_page, "Page count:", self.page_count)
        if self.current_page > 0:
            self.current_page -= 1
            self.update_displayed_results()
        
    def on_next_clicked(self) -> None:
        print("[Next] Current page:", self.current_page, "Page count:", self.page_count)
        if self.current_page < self.page_count - 1:
            self.current_page += 1
            self.update_displayed_results()