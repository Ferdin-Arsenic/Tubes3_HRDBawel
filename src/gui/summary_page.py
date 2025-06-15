# src/gui/summary_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class SummaryPage(QWidget):
    back_button_clicked = pyqtSignal()  # Tambahkan signal ini
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setStyleSheet("background-color: #d9d9d9;")

        # Tombol kembali, kita letakkan di atas untuk konsistensi
        self.back_button = QPushButton("← Kembali")
        self.back_button.setFixedWidth(100)
        self.back_button.clicked.connect(self.back_button_clicked.emit)  # Connect signal
        
        # Judul halaman
        self.title_label = QLabel("Ringkasan CV")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Area teks untuk menampilkan konten ringkasan
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        text_font = QFont()
        text_font.setPointSize(12)
        self.summary_text.setFont(text_font)
        
        # Tambahkan widget ke layout
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_text)

    def set_summary_data(self, title: str, summary_text: str):
        """Metode untuk mengisi data ke halaman ini."""
        self.title_label.setText(title)
        self.summary_text.setPlainText(summary_text)