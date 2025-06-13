from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from gui.applicant_card import ApplicantCard
from models.search import ApplicantMatchData

class ResultDisplay(QWidget):
    view_summary = pyqtSignal(int)  # Signal to view summary
    view_cv = pyqtSignal(int)       # Signal to view CV (launch a window with the CV PDF)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize widgets that is put into two pages
        self.stack = QStackedWidget()
        pages_layout = QVBoxLayout(self)
        pages_layout.setContentsMargins(0,0,0,0)
        pages_layout.addWidget(self.stack)
        
        # Set pagination
        self.page_count = 0
        self.current_page = 0
        self.results_per_page = 4

        # Set the layout for blank state before anyy result is shown
        self.result_cards: list[QStackedWidget] = [QStackedWidget() for _ in range(self.results_per_page)]

        self.initialize_widgets(self.stack)
        # TESTING FOR THIS. DELETEEEEEEEEEEEEEEEEEEEEE
        test_data: list[ApplicantMatchData] = [
            ApplicantMatchData(detail_id=i, name=f"Applicant {i}", match_count=i+1, matched_keywords={"python":1}) for i in range(10)
        ]
        self.set_results(test_data)
        self.stack.setCurrentWidget(self.result_page)

    """ Page Builder """
    def initialize_widgets(self, page_stack:QStackedWidget) -> None:
        self.blank_page = QWidget()
        self.result_page = QWidget()
        page_stack.addWidget(self.blank_page)
        page_stack.addWidget(self.result_page)
        self.initialize_widgets_result_page()
        self.initialize_widgets_blank_page()

    def initialize_widgets_result_page(self) -> None:
        # 5x6 grid
        self.result_page.setContentsMargins(0, 0, 0, 0)
        self.result_page.setStyleSheet("color: #000000;")
        container = QGridLayout(self.result_page)
        container.setContentsMargins(0, 5, 0, 5)
        container.setSpacing(0)
        container.setRowStretch(2, 1)
        container.setRowMinimumHeight(3, 10)
        container.setRowStretch(4, 1)
        container.setColumnMinimumWidth(0, 25)
        container.setColumnStretch(1, 1)
        container.setColumnStretch(3, 1)
        container.setColumnMinimumWidth(4, 25)

        left_button = QPushButton("◀", clicked=self.on_prev_clicked)
        left_button.setStyleSheet("font-size: 25px;")
        left_button.setMaximumWidth(25)
        container.addWidget(left_button, 0, 0, -1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        right_button = QPushButton("▶", clicked=self.on_next_clicked)
        right_button.setStyleSheet("font-size: 25px;")
        right_button.setMaximumWidth(25)
        container.addWidget(right_button, 0, 4, -1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        result_summary = QLabel("5 applicants found")
        result_summary.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; font-weight: bold;")
        container.addWidget(result_summary, 0, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)
        search_statistics = QLabel("searched 100 CVs under 100ms")
        search_statistics.setStyleSheet("font-size: 10px; font-family: Inter, sans-serif; margin: 0px 0px 5px 0px;")
        container.addWidget(search_statistics, 1, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)

        page_label = QLabel("0/0")
        page_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #444444;")
        container.addWidget(page_label, 5, 1, -1, 3, Qt.AlignmentFlag.AlignCenter)

        # Place applicant card stacks
        cards_columns = [1, 3]
        cards_rows = [2, 4]
        columns_count = len(cards_columns)
        for i, stack_widget in enumerate(self.result_cards):
            row = cards_rows[i // columns_count]
            col = cards_columns[i % columns_count]

            container.addWidget(stack_widget, row, col, 1, 1, Qt.AlignmentFlag.AlignLeft)

    def initialize_widgets_blank_page(self) -> None:
        self.blank_page.setStyleSheet("background-color: #f0f0f0; color: #000000;")        
        blank_layout = QVBoxLayout(self.blank_page)
        blank_layout.setContentsMargins(5, 5, 5, 5)
        blank_layout.setSpacing(0)
        blank_label = QLabel("Search for applicants to see results here")
        blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        blank_label.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; color: #888888;")
        blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        blank_layout.addWidget(blank_label)

    """ Controls """
    def clear_results(self) -> None:
        self.set_results([])  # Clear the results by setting an empty list
        self.pages.setCurrentWidget(self.blank_page)
    
    def display_results(self) -> None:
        if not self.result_cards:
            self.clear_results()
            return
        
        # Paginate the results by shifting through the stacked widgets
        for card_stack in self.result_cards:
            widget = card_stack.widget(self.current_page-1)
            card_stack.setCurrentWidget(widget)

        # self.stack.setCurrentWidget(self.result_page)

    def set_results(self, results: list[ApplicantMatchData]) -> None:
        self.page_count = (len(results) + self.results_per_page - 1) // self.results_per_page
        self.current_page = 1 if self.page_count > 0 else 0
        
        for stack in self.result_cards:
            while stack.count() > 0:
                widget = stack.widget(0)
                stack.removeWidget(widget)
                widget.deleteLater()
        for i in range(self.page_count * self.results_per_page):
            if i < len(results):
                card = ApplicantCard(results[i])
                card.view_summary.connect(self.view_summary)
                card.view_cv.connect(self.view_cv)
                self.result_cards[i % self.results_per_page].addWidget(card)
            else:
                blank_space = QWidget()
                self.result_cards[i % self.results_per_page].addWidget(blank_space)

    def on_prev_clicked(self) -> None:
        print("[Prev] Current page:", self.current_page, "Page count:", self.page_count)
        if self.current_page > 1:
            self.current_page -= 1
            self.display_results()
        
    def on_next_clicked(self) -> None:
        print("[Next] Current page:", self.current_page, "Page count:", self.page_count)
        if self.current_page < self.page_count:
            self.current_page += 1
            self.display_results()