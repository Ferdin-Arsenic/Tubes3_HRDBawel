from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QGridLayout, QSpacerItem,QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from gui.applicant_card import ApplicantCard
from models.search import SearchResult

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
        container.setRowMinimumHeight(0, 25)
        container.setRowMinimumHeight(1, 25)
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
        container.addWidget(left_button, 2, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        right_button = QPushButton("▶", clicked=self.on_next_clicked)
        right_button.setStyleSheet("font-size: 25px;")
        right_button.setMaximumWidth(25)
        container.addWidget(right_button, 2, 4, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.result_summary = QLabel("5 applicants found")
        self.result_summary.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; font-weight: bold;")
        container.addWidget(self.result_summary, 0, 1, 1, 3, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.search_statistics = QLabel("searched 100 CVs under 100ms")
        self.search_statistics.setStyleSheet("font-size: 10px; font-family: Inter, sans-serif; margin: 0px 0px 5px 0px;")
        container.addWidget(self.search_statistics, 1, 1, 1, 3, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.page_label = QLabel("0 / 0")
        self.page_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #444444; margin: 0px;")
        container.addWidget(self.page_label, 5, 1, -1, 3, Qt.AlignmentFlag.AlignCenter)

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
        blank_layout.setContentsMargins(0, 0, 0, 0)
        blank_layout.setSpacing(0)
        
        self.blank_label = QLabel("Search for applicants to see results here")
        self.blank_label.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; color: #9a9a9a;")
        self.blank_sublabel = QLabel("Start by entering keywords in the left panel")
        self.blank_sublabel.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #9a9a9a;")
        
        blank_layout.addStretch(1)
        blank_layout.addWidget(self.blank_label, 0, Qt.AlignmentFlag.AlignHCenter)
        blank_layout.addWidget(self.blank_sublabel, 0, Qt.AlignmentFlag.AlignHCenter)
        blank_layout.addStretch(1)

    """ Controls """
    def clear_results(self, empty_result: bool = False) -> None:
        if empty_result:
            self.blank_label.setText("No applicant found")
            self.blank_sublabel.setText(self.search_statistics.text())
        else:
            self.blank_label.setText("Search for applicants to see results here")
            self.blank_sublabel.setText("Start by entering keywords in the left panel")
            self.set_results(SearchResult([], 0, 0))  # Clear the results by setting an empty list
        self.stack.setCurrentWidget(self.blank_page)
        print("Cleared results and switched to blank page.")
    
    def display_results(self) -> None:
        if self.page_count == 0 or self.current_page == 0:
            self.clear_results(True)
        else:    
            # Paginate the results by shifting through the stacked widgets
            for card_stack in self.result_cards:
                widget = card_stack.widget(self.current_page-1)
                card_stack.setCurrentWidget(widget)
            self.stack.setCurrentWidget(self.result_page)

    def set_results(self, results: SearchResult) -> None:
        self.page_count = (len(results.applicants) + self.results_per_page - 1) // self.results_per_page
        self.current_page = 1 if self.page_count > 0 else 0
        
        self.page_label.setText(f"{self.current_page} / {self.page_count}")
        self.result_summary.setText(f"{len(results.applicants)} applicants found")
        if results.fuzzy_runtime > 0:
            self.search_statistics.setText(f"searched {results.cvs_scanned} CVs under {results.runtime:.0f}ms, with fuzzy search under {results.fuzzy_runtime:.0f}ms")
        else:
            self.search_statistics.setText(f"searched {results.cvs_scanned} CVs under {results.runtime:.0f}ms")
        print(self.search_statistics.text())

        for stack in self.result_cards:
            while stack.count() > 0:
                widget = stack.widget(0)
                stack.removeWidget(widget)
                widget.deleteLater()
        for i in range(self.page_count * self.results_per_page):
            if i < len(results.applicants):
                card = ApplicantCard(results.applicants[i])
                card.view_summary.connect(self.view_summary)
                card.view_cv.connect(self.view_cv)
                self.result_cards[i % self.results_per_page].addWidget(card)
            else:
                blank_space = QWidget()
                self.result_cards[i % self.results_per_page].addWidget(blank_space)

    def on_prev_clicked(self) -> None:
        if self.current_page > 1:
            self.current_page -= 1
            self.display_results()
            self.page_label.setText(f"{self.current_page} / {self.page_count}")
        
    def on_next_clicked(self) -> None:
        if self.current_page < self.page_count:
            self.current_page += 1
            self.display_results()
            self.page_label.setText(f"{self.current_page} / {self.page_count}")