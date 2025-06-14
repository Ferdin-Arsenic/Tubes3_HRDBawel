import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from gui.applicant_card import ApplicantCard
from models.search import ApplicantMatchData

class ResultDisplay(QWidget):
    view_summary = pyqtSignal(int)
    view_cv = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("color: #000000;")

        # --- Atribut untuk data dan paginasi ---
        self.all_results: list[ApplicantMatchData] = []
        self.page_count = 0
        self.current_page = 0
        self.results_per_page = 4

        # --- Setup Widget dan Layout (Struktur Final yang Benar dan Bersih) ---

        # 1. Label untuk state awal (saat belum ada hasil)
        self.blank_label = QLabel("Search for applicants to see results here")
        self.blank_label.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; color: #444444;")
        self.blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 2. Widget utama yang menampung semua elemen hasil pencarian
        self.results_widget = QWidget()
        
        main_results_layout = QVBoxLayout(self.results_widget)
        main_results_layout.setSpacing(5)

        # 2a. Label Waktu Eksekusi
        self.timing_label = QLabel("")
        self.timing_label.setStyleSheet("font-size: 11px; font-family: Inter, sans-serif; color: #555555;")
        self.timing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_results_layout.addWidget(self.timing_label)

        # 2b. Layout horizontal untuk baris hasil (tombol navigasi + kartu)
        results_row_layout = QHBoxLayout()
        
        left_button = QPushButton("◀", clicked=self.on_prev_clicked)
        left_button.setStyleSheet("font-size: 25px; border: none; background: transparent;")
        left_button.setFixedWidth(25)
        results_row_layout.addWidget(left_button, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.result_card_layout = QGridLayout()
        self.result_card_layout.setSpacing(10)
        results_row_layout.addLayout(self.result_card_layout)

        right_button = QPushButton("▶", clicked=self.on_next_clicked)
        right_button.setStyleSheet("font-size: 25px; border: none; background: transparent;")
        right_button.setFixedWidth(25)
        results_row_layout.addWidget(right_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        main_results_layout.addLayout(results_row_layout)
        
        # 2c. Label Halaman
        self.page_label = QLabel("0/0")
        self.page_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #444444;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_results_layout.addWidget(self.page_label)

        main_results_layout.addStretch()

        # 3. Layout root yang mengatur mana yang ditampilkan
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.blank_label)
        root_layout.addWidget(self.results_widget)
        
        self.results_widget.hide()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.clear_layout(sub_layout)

    def update_displayed_results(self):
        self.clear_layout(self.result_card_layout)
        start_index = self.current_page * self.results_per_page
        end_index = start_index + self.results_per_page
        results_to_display = self.all_results[start_index:end_index]

        row, col = 0, 0
        for data in results_to_display:
            card = ApplicantCard(data)
            card.view_summary.connect(self.view_summary)
            card.view_cv.connect(self.view_cv)
            self.result_card_layout.addWidget(card, row, col)
            col = (col + 1) % 2
            if col == 0:
                row += 1
        self.page_label.setText(f"Page {self.current_page + 1}/{self.page_count}")

    def set_results(self, results: list[ApplicantMatchData], exact_time: float, fuzzy_time: float):
        self.all_results = results
        timing_text = f"Exact Match: found results in {exact_time:.2f}ms."
        if fuzzy_time > 0:
            timing_text += f"\nFuzzy Match: ran in {fuzzy_time:.2f}ms."
        self.timing_label.setText(timing_text)
        
        if not results:
            self.results_widget.hide()
            self.blank_label.setText("No matching applicants found.")
            self.blank_label.show()
            return

        self.blank_label.hide()
        self.results_widget.show()
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