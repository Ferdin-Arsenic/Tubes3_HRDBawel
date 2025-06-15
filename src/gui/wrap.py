from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class HorizontalWrapGroup(QWidget):
    def __init__(self, width: int, parent=None):
        super().__init__(parent)
        
        self.width = width
        self.space_between = 10
        self.setFixedWidth(width)
        self.rows_layout = QVBoxLayout(self)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(self.space_between)

        self.row_layouts: list[QHBoxLayout] = [] # row_layout
        self.row_space_used: list[int] = []  # total occupied width including space_between used in each row

        # Dummy widgets
        self.set_widgets([QLabel("Skill "+str(i)) for i in range(1, 6)])
    
    def set_widgets(self, widgets: list[QWidget]) -> None:
        if not widgets:
            return
        for row_layout in self.row_layouts:
            while row_layout.count():
                item = row_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.rows_layout.removeItem(row_layout)
            row_layout.deleteLater()
        self.row_layouts.clear()
        self.row_space_used.clear()

        self.row_layouts.append(QHBoxLayout())
        self.row_space_used.append(0)
        for widget in widgets:
            if (self.row_space_used[-1] + widget.sizeHint().width() + self.space_between) > self.width:
                # Start a new row if the current one exceeds the width
                self.row_layouts.append(QHBoxLayout())
                self.row_space_used.append(0)
                self.row_layouts[-1].addWidget(widget)
                self.row_space_used[-1] += widget.sizeHint().width()
            else:
                # Add to the current row
                self.row_layouts[-1].addWidget(widget)
                self.row_space_used[-1] += self.space_between + widget.sizeHint().width() 
        
        for row_layout in self.row_layouts:
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(self.space_between)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.rows_layout.addLayout(row_layout)