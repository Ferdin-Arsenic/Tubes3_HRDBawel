import PyQt6.QtWidgets as QWidgets
from gui.search_page import InputFields

class App(QWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        # Root widget
        self.root = QWidgets.QWidget()
        self.root.resize(640, 400)
        self.root.setWindowTitle("Application Tracking System - HRDBawel")
        
        root_layout = QWidgets.QHBoxLayout(self.root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)


        # Left panel
        self.left_panel = QWidgets.QWidget()
        self.left_panel.setStyleSheet("background-color: #c9f5a2;")
        self.left_panel.setFixedWidth(265)

        left_layout = QWidgets.QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)


        # Right panel
        self.right_panel = QWidgets.QWidget()
        self.right_panel.setStyleSheet("background-color: #d9d9d9;")
        
        right_layout = QWidgets.QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)


        # Add widgets to the layouts
        root_layout.addWidget(self.left_panel)
        root_layout.addWidget(self.right_panel)


        # Input fields in the left panel
        self.input_fields = InputFields(self.left_panel)
        left_layout.addWidget(self.input_fields)
    
