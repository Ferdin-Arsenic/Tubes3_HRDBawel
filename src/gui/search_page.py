from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from gui.input import InputFields
from gui.result import ResultDisplay
from models.search import SearchParams

class SearchPage(QWidget):
    search_initiate = pyqtSignal(SearchParams)  # Signal to initiate search with parameters
    view_summary = pyqtSignal(int)  # Signal to view summary
    view_cv = pyqtSignal(int)       # Signal to view CV (launch a window with the CV PDF)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Left panel
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #c9f5a2;")
        left_panel.setFixedWidth(265)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Right panel
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #d9d9d9;")
        right_panel.setFixedWidth(375)
        right_panel.setContentsMargins(0, 0, 0, 0)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Add widgets to the layouts
        root_layout.addWidget(left_panel)
        root_layout.addWidget(right_panel)


        # Input fields in the left panel
        input_fields = InputFields(left_panel)
        input_fields.search_initiate.connect(self.search_initiate)

        # Result display in the right panel
        result_display = ResultDisplay(right_panel)
        result_display.view_summary.connect(self.view_summary)
        result_display.view_cv.connect(self.view_cv)

        left_layout.addWidget(input_fields)
        right_layout.addWidget(result_display)