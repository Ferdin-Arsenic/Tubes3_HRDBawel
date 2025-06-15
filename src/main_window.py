from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from gui.search_page import SearchPage
from gui.summary_page import SummaryPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Tracking System ")
        self.setFixedSize(640, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.search_page = SearchPage()
        self.summary_page = SummaryPage()
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.summary_page)

        self.search_page.search_initiate.connect(self.search)
        self.search_page.view_summary.connect(self.summary)
        self.search_page.view_cv.connect(self.view_cv)

        self.summary_page.return_from_summary.connect(self.return_to_search)

        # Dummy data for testing
        from models.search import SearchResult, ApplicantMatchData
        test_data: list[ApplicantMatchData] = [
            ApplicantMatchData(detail_id=i, name=f"Applicant {i}", match_count=i+1, matched_keywords={"python":1}) for i in range(10)
        ]
        self.search_page.show_results(SearchResult(applicants=test_data, cvs_scanned=102, runtime=100))

    def search(self, search_params: dict):
        print("Search initiated with parameters:", search_params)
        # Compute

    def view_cv(self, detail_id: id):
        print(f"Viewing CV for applicant ID: {detail_id}")
        # Show CV pdf

    def summary(self, detail_id: id):
        # TO DO: Dummy page. INTEGRATE NEXT
        from models.search import WorkExperienceEntry, EducationEntry, CVSummary
        from datetime import datetime
        self.summary_page.set_summary(1, CVSummary(
            name="John Doe",
            birthdate= datetime(1990, 1, 1),
            address="123 Main St, City",
            contacts=["+6281234567890", "absc.xyz"],
            description="A brief summary of the applicant's qualifications and experience.",
            skills=["Python", "Java", "C++", "Machine Learning", "Data Analysis"],
            education=[EducationEntry(
                institution="University XYZ",
                program="Bachelor of Science in Computer Science",
                start_date="2010-01",
                end_date="2014-01"
            )],
            work_experience=[
                WorkExperienceEntry(
                    company="Company ABC",
                    position="Software Engineer",
                    start_date="2015-01",
                    end_date="2020-01",
                    description="Developed and maintained software applications using Python and Java."
                ),
                WorkExperienceEntry(
                    company="Company XYZ",
                    position="Senior Developer",
                    description="",
                    start_date="2020-01",
                    end_date="2023-01"
                )
            ]
        ))
        self.stack.setCurrentWidget(self.summary_page)
        # Extracted CV summary

    def return_to_search(self):
        self.stack.setCurrentWidget(self.search_page)
        self.search_page.setFocus()
