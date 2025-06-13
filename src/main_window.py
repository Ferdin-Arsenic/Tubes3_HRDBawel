from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from gui.search_page import SearchPage
from gui.summary_page import SummaryPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Tracking System ")
        self.resize(640, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.search_page = SearchPage()
        self.summary_page = SummaryPage()
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.summary_page)

        self.search_page.search_initiate.connect(self.search)
        self.search_page.view_summary.connect(self.summary)
        self.search_page.view_cv.connect(self.view_cv)

    def search(self, search_params: dict):
        print("Search initiated with parameters:", search_params)
        # Compute

    def view_cv(self, detail_id: id):
        print(f"Viewing CV for applicant ID: {detail_id}")
        # Show CV pdf

    def summary(self, detail_id: id):
        print(f"Viewing summary for applicant ID: {detail_id}")
        # Extracted CV summary
