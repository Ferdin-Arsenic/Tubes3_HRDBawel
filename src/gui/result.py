from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from gui.applicant_card import ApplicantCard
from models.search import ApplicantMatchData
import math

class ResultDisplay(QWidget):
    view_summary = pyqtSignal(int)
    view_cv = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("color: #000000;")

        self.all_results: list[ApplicantMatchData] = []
        self.page_count = 0
        self.current_page = 0
        self.results_per_page = 4

        # Layout utama dan widget
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.timing_label = QLabel("")
        self.timing_label.setStyleSheet("font-size: 11px; font-family: Inter, sans-serif; color: #555555;")
        self.timing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.timing_label)

        # Container untuk kartu hasil dan tombol navigasi
        self.results_container = QWidget()
        self.container = QGridLayout(self.results_container)
        self.container.setRowMinimumHeight(0, 350) # Set tinggi untuk baris kartu

        # Layout untuk kartu-kartu
        self.result_card_layout = QGridLayout()
        self.result_card_layout.setSpacing(10)
        self.container.addLayout(self.result_card_layout, 0, 1)

        # Tombol navigasi
        left_button = QPushButton("◀", clicked=self.on_prev_clicked)
        left_button.setStyleSheet("font-size: 25px; border: none;")
        left_button.setFixedWidth(25)
        self.container.addWidget(left_button, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        right_button = QPushButton("▶", clicked=self.on_next_clicked)
        right_button.setStyleSheet("font-size: 25px; border: none;")
        right_button.setFixedWidth(25)
        self.container.addWidget(right_button, 0, 2, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.main_layout.addWidget(self.results_container)

        # Label Halaman
        self.page_label = QLabel("0/0")
        self.page_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #444444;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.page_label)

        # State awal (kosong)
        self.blank_label = QLabel("Search for applicants to see results here")
        self.blank_label.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; color: #444444;")
        self.blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.blank_label)

        self.results_container.hide()
        self.page_label.hide()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def update_displayed_results(self):
        self.clear_layout(self.result_card_layout)

        start_index = self.current_page * self.results_per_page
        end_index = start_index + self.results_per_page
        results_to_display = self.all_results[start_index:end_index]

        # Buat kartu untuk setiap hasil di halaman ini
        row, col = 0, 0
        for data in results_to_display:
            card = ApplicantCard(data)
            card.view_summary.connect(self.view_summary)
            card.view_cv.connect(self.view_cv)
            self.result_card_layout.addWidget(card, row, col)
            
            col += 1
            if col % 1 == 0: # 2 kartu per baris
                col = 0
                row += 1

        self.page_label.setText(f"Page {self.current_page + 1}/{self.page_count}")

    def set_results(self, results: list[ApplicantMatchData], exact_time: float, fuzzy_time: float):
        self.all_results = results

        # Update label waktu
        timing_text = f"Exact Match: {len(self.all_results)} CVs scanned in {exact_time:.4f}s."
        if fuzzy_time > 0:
            timing_text += f"\nFuzzy Match: ran in {fuzzy_time:.4f}s."
        self.timing_label.setText(timing_text)
        
        if not results:
            self.results_container.hide()
            self.page_label.hide()
            self.blank_label.setText("No matching applicants found.")
            self.blank_label.show()
            return

        self.blank_label.hide()
        self.results_container.show()
        self.page_label.show()

        self.current_page = 0
        self.page_count = math.ceil(len(self.all_results) / self.results_per_page)
        self.update_displayed_results()

    def on_prev_clicked(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self.update_displayed_results()
        
    def on_next_clicked(self) -> None:
        if self.current_page < self.page_count - 1:
            self.current_page += 1
            self.update_displayed_results()