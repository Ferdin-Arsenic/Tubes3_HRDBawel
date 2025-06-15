from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import time
import os
import re
from datetime import datetime
from gui.search_page import SearchPage
from gui.summary_page import SummaryPage
from models.search import SearchParams, ApplicantMatchData, ApplicationDetail, SearchResult, SearchAlgorithm, WorkExperienceEntry, EducationEntry, CVSummary

from lib.kmp import KMP
from lib.bm import BM
from lib.aho_corasick import aho_corasick
from lib.levenshtein import levenshtein_distance
from database.cv_database import CVDatabase
from util.parser import pdf_to_string

algorithm_map = {
    SearchAlgorithm.KMP: KMP,
    SearchAlgorithm.BM: BM,
    SearchAlgorithm.AHO_CORASICK: aho_corasick,
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Tracking System ")
        self.setFixedSize(640, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize database with error handling
        try:
            print("Initializing database...")
            self.db = CVDatabase()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization failed: {e}")
            self.db = None

        print("Creating search page...")
        self.search_page = SearchPage()
        print("Creating summary page...")
        self.summary_page = SummaryPage()
        
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.summary_page)

        # Connect signals
        print("Connecting signals...")
        self.search_page.search_initiate.connect(self.search)
        self.search_page.view_summary.connect(self.summary)
        self.search_page.view_cv.connect(self.view_cv)
        self.summary_page.return_from_summary.connect(self.return_to_search)

    def show_search_page(self):
        """Method untuk kembali ke halaman search"""
        self.stack.setCurrentWidget(self.search_page)


    def search(self, search_params: SearchParams):
        search_results = SearchResult(applicants=[], cvs_scanned=0, runtime=0)
        applications = self.db.get_all_application_details()

        # Compute a mapping of detail_id to ApplicantMatchData
        app_matches = self.exact_search(search_params, search_results, applications)

        each_keyword_found = False
        for keyword in search_params.keywords:
            for match in app_matches.values():
                if keyword in match.matched_keywords:
                    each_keyword_found = True
                    break

        if not each_keyword_found or len(search_results.applicants) < search_params.top_matches:
            # Compute additional matches using fuzzy search
            self.fuzzy_search(search_params, search_results, applications, app_matches)

        # Aggregate app_matches into SearchResult
        for detail_id, match_data in app_matches.items():
            profile = self.db.get_applicant_profile(detail_id)
            if profile:
                match_data.name = f"{profile.first_name} {profile.last_name}"
                search_results.applicants.append(match_data)

        # Sort the results by match count in descending order
        search_results.applicants.sort(key=lambda x: x.match_count, reverse=True)
        self.search_page.show_results(search_results)

    def exact_search(self, search_params: SearchParams, search_results: SearchResult, applications: list[ApplicationDetail]) -> dict[int, ApplicantMatchData]:
        print(f"Performing exact search with parameters: {search_params}")
        
        search_function = algorithm_map.get(search_params.algorithm)

        final_results: dict[int, ApplicantMatchData] = {}
        start_time = time.time()
        for app in applications:
            cv_text = pdf_to_string(app.cv_path).lower() if app.cv_path else ""
            exact_matches: dict[str, int] = {}
            if search_params.algorithm == SearchAlgorithm.AHO_CORASICK:
                matches = aho_corasick(cv_text, search_params.keywords)
                exact_matches = {k: len(v) for k, v in matches.items() if v}
            else:
                for keyword in search_params.keywords:
                    keyword_lower = keyword.strip().lower()
                    if not keyword_lower: continue

                    occurrences = search_function(cv_text, keyword_lower)
                    if occurrences:
                        exact_matches[keyword] = len(occurrences)
            
            if exact_matches:
                final_results[app.detail_id] = ApplicantMatchData(
                    detail_id=app.detail_id,
                    name="",  # Filled later
                    match_count = sum(exact_matches.values()),
                    matched_keywords=exact_matches,
                )
        end_time = time.time()
        
        search_results.cvs_scanned = len(applications)
        search_results.runtime = (end_time - start_time) * 1000
        return final_results

    def fuzzy_search(self, search_params: SearchParams, search_results: SearchResult, applications: list[ApplicationDetail], previous_matches: dict[int, ApplicantMatchData]) -> None:
        print(f"Performing fuzzy search with parameters: {search_params}")
        SIMILARITY_THRESHOLD = 80.0

        start_time = time.time()
        for app in applications:
            cv_text = pdf_to_string(app.cv_path).lower() if app.cv_path else ""
            fuzzy_matches: dict[str, int] = {}
            for keyword in search_params.keywords:
                keyword_lower = keyword.strip().lower()
                if not keyword_lower: continue
                
                words_in_cv = set(re.findall(r'[a-z]+', cv_text))
                for word_in_cv in words_in_cv:
                    len_max = max(len(keyword_lower), len(word_in_cv))
                    if len_max > 0:
                        distance = levenshtein_distance(keyword_lower, word_in_cv)
                        similarity = (1 - (distance / len_max)) * 100
                        if SIMILARITY_THRESHOLD <= similarity < 100:
                            fuzzy_key = f"{word_in_cv} (~)"
                            fuzzy_matches[fuzzy_key] = fuzzy_matches.get(fuzzy_key, 0) + 1
            
            if fuzzy_matches:
                detail_id = app.detail_id
                if detail_id in previous_matches:
                    match_data = previous_matches[detail_id]
                    match_data.match_count += sum(fuzzy_matches.values())
                    match_data.fuzzy_matched_keywords = fuzzy_matches
                else:
                    match_data = ApplicantMatchData(
                        detail_id=detail_id,
                        name="",  # Filled later
                        match_count=sum(fuzzy_matches.values()),
                        matched_keywords={},
                        fuzzy_matched_keywords=fuzzy_matches
                    )
                    previous_matches[detail_id] = match_data
        end_time = time.time()

        search_results.cvs_scanned = len(applications)
        search_results.fuzzy_runtime = (end_time - start_time) * 1000

    def view_cv(self, detail_id: str):
        """
        Finds the PDF file path from the database using the detail_id
        and opens it with the default system PDF viewer.
        """
        print(f"Attempting to view CV for applicant ID: {detail_id}")
        
        # Get the relative path of the PDF from the database
        pdf_relative_path = self.db.get_cv_path(detail_id)

        if pdf_relative_path:
            # Construct the absolute path. This assumes the script is run from the project root.
            # A more robust way might be needed if the execution path changes.
            base_dir = os.path.abspath(os.path.dirname(__file__) + "/..")
            pdf_full_path = os.path.join(base_dir, pdf_relative_path)
            
            print(f"Found PDF at: {pdf_full_path}")

            if os.path.exists(pdf_full_path):
                # Open the PDF file using the system's default application
                url = QUrl.fromLocalFile(pdf_full_path)
                QDesktopServices.openUrl(url)
            else:
                print(f"Error: PDF file not found at path: {pdf_full_path}")
        else:
            print(f"Error: Could not find a CV path for ID: {detail_id}")

    def summary(self, detail_id: id):
        app_detail = self.db.get_application_detail(detail_id)
        app_profile = self.db.get_applicant_profile(app_detail.applicant_id)
        cv_summary = CVSummary(
            name = app_profile.first_name + " " + app_profile.last_name,
            birthdate = app_profile.date_of_birth,
            address = app_profile.address,
            contacts = [app_profile.phone_number],
            description = "",
            skills = [],
            education = [],
            work_experience = []
        )

        # TO DO: Dummy page. INTEGRATE NEXT
        # Dummy data for testing
        cv_summary.description = "A brief summary of the applicant's qualifications and experience."
        cv_summary.skills = ["Python", "Java", "C++", "Machine Learning", "Data Analysis"]
        cv_summary.education = [
            EducationEntry(
                institution="University XYZ",
                program="Bachelor of Science in Computer Science",
                start_date="2010-01",
                end_date="2014-01"
            )
        ]
        cv_summary.work_experience = [
            WorkExperienceEntry(
                position="Software Engineer",
                company="Company ABC",
                start_date="2015-01",
                end_date="2020-01",
                description="Developed and maintained software applications using Python and Java."
            ),
            WorkExperienceEntry(
                position="Senior Developer",
                company="",
                description="",
                start_date="2020-01",
                end_date=""
            )
        ]

        self.summary_page.set_summary(detail_id, cv_summary)
        self.stack.setCurrentWidget(self.summary_page)
        # Extracted CV summary

    def return_to_search(self):
        self.stack.setCurrentWidget(self.search_page)
        self.search_page.setFocus()
