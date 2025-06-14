from PyQt6.QtWidgets import QWidget, QFrame, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from models.search import ApplicantMatchData

class ApplicantCard(QWidget):
    view_summary = pyqtSignal(int)
    view_cv = pyqtSignal(int)

    def __init__(self, data: ApplicantMatchData, parent=None):
        super().__init__(parent)
        self.detail_id = data.detail_id

        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(155)
        self.setFixedWidth(155)
        self.setStyleSheet("border-radius: 10px; background-color: #ffffff;")
        self.background_layout = QVBoxLayout(self)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        self.container_widget = QWidget()
        self.background_layout.addWidget(self.container_widget)
        self.container = QVBoxLayout(self.container_widget)
        self.initialize_widgets(data)

    def initialize_widgets(self, data: ApplicantMatchData) -> None:
        self.container.setContentsMargins(0, 10, 0, 5)
        self.container.setSpacing(0)

        name_label = QLabel(data.name)
        name_label.setStyleSheet("font-size: 12px; font-weight: bold; font-family: Inter, sans-serif; color: #000000; margin: 0px 5px 10px 5px;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container.addWidget(name_label)

        match_count_label = QLabel(f"{data.match_count} matches")
        match_count_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #000000; margin-left: 5px;")
        match_count_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container.addWidget(match_count_label)

        keywords_table = KeywrodsMatchedTable(data)
        keywords_table.setStyleSheet("background-color: #ffffff; color: #000000; border: none; margin-left: 5px;")
        self.container.addWidget(keywords_table)

        horizontal_line = QWidget()
        horizontal_line.setFixedHeight(1)
        horizontal_line.setStyleSheet("background-color: #cccccc;")
        self.container.addWidget(horizontal_line)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 5, 0, 0)
        buttons_layout.setSpacing(5)
        self.container.addLayout(buttons_layout)

        summary_button = QPushButton("Summary", clicked=lambda: self.view_summary.emit(self.detail_id))
        summary_button.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #000000; background-color: transparent;")
        summary_button.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons_layout.addWidget(summary_button)

        cv_button = QPushButton("View CV", clicked=lambda: self.view_cv.emit(self.detail_id))
        cv_button.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #000000; border: none; background-color: transparent;")
        cv_button.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons_layout.addWidget(cv_button)

class KeywrodsMatchedTable(QTableWidget):
    def __init__(self, data: ApplicantMatchData, parent=None):
        super().__init__(parent)
        self.setRowCount(len(data.matched_keywords))
        self.setColumnCount(2)
        self.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #000000; border: none;")
        self.setFixedWidth(150)
        self.setShowGrid(False)
        self.setContentsMargins(0, 0, 0, 0)

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setColumnWidth(0, 115)
        self.setColumnWidth(1, 10)
        font_metrics = self.fontMetrics()
        row_height = font_metrics.height()
        for row, (keyword, freq) in enumerate(data.matched_keywords.items()):
            keyword_item = QTableWidgetItem(keyword)
            keyword_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            freq_item = QTableWidgetItem(str(freq))
            freq_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, 0, keyword_item)
            self.setItem(row, 1, freq_item)
            self.setRowHeight(row, row_height)