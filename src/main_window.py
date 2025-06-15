from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import time
import os
import re
from gui.search_page import SearchPage
from gui.summary_page import SummaryPage
from models.search import SearchParams, ApplicantMatchData, SearchResult
from models.search import SearchAlgorithm 

from lib.kmp import KMP
from lib.bm import BM
from lib.aho_corasick import aho_corasick
from lib.levenshtein import levenshtein_distance
from database.cv_database import CvDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Tracking System ")
        self.resize(640, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize database with error handling
        try:
            print("Initializing database...")
            self.db = CvDatabase()
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
        print("MainWindow initialization complete")

    def show_search_page(self):
        """Method untuk kembali ke halaman search"""
        self.stack.setCurrentWidget(self.search_page)

    def search(self, search_params: SearchParams):
        start_time = time.time()

        algorithm_map = {
            SearchAlgorithm.KMP: KMP,
            SearchAlgorithm.BM: BM,
            SearchAlgorithm.AHO_CORASICK: aho_corasick,
        }
        search_function = algorithm_map.get(search_params.algorithm)
        
        if not search_params.keywords or not search_params.keywords[0]:
            self.search_page.result_display.clear_results(empty_result=False)
            return

        base_dir = os.path.dirname(os.path.dirname(__file__))
        text_files_dir = os.path.join(base_dir, "dataset", "txt")
        if not os.path.isdir(text_files_dir):
            print(f"Error: Directory not found at {text_files_dir}")
            return
            
        all_files = [f for f in os.listdir(text_files_dir) if f.endswith(".txt")]
        final_results_map = {}

        for filename in all_files:
            applicant_id = os.path.splitext(filename)[0]
            file_path = os.path.join(text_files_dir, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
            except (IOError, FileNotFoundError):
                continue

            exact_matches = {}
            for keyword in search_params.keywords:
                keyword_lower = keyword.strip().lower()
                if not keyword_lower: continue

                occurrences = search_function(content, keyword_lower)
                if occurrences:
                    exact_matches[keyword] = len(occurrences)
            
            if exact_matches:
                final_results_map[applicant_id] = ApplicantMatchData(
                    detail_id=int(applicant_id),
                    name=f"Applicant {applicant_id}",
                    match_count=sum(exact_matches.values()),
                    matched_keywords=exact_matches,
                )

        if final_results_map:
            end_time = time.time()
            runtime_ms = (end_time - start_time) * 1000
            print(f"Search complete in {runtime_ms:.2f} ms. Found {len(final_results_map)} matching applicants (Exact).")
            
            sorted_results = sorted(final_results_map.values(), key=lambda x: x.match_count, reverse=True)
            top_results = sorted_results[:search_params.top_matches]
            self.search_page.result_display.set_results(SearchResult(
                applicants=top_results,
                cvs_scanned=len(all_files),
                runtime=runtime_ms
            ), is_fuzzy=False)
            return

        SIMILARITY_THRESHOLD = 80.0
        fuzzy_results_map = {}

        for filename in all_files:
            applicant_id = os.path.splitext(filename)[0]
            file_path = os.path.join(text_files_dir, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    words_in_cv = set(re.findall(r'[a-z]+', content))
            except (IOError, FileNotFoundError):
                continue
            
            fuzzy_matches = {}
            for keyword in search_params.keywords:
                keyword_lower = keyword.strip().lower()
                if not keyword_lower: continue
                
                for word_in_cv in words_in_cv:
                    len_max = max(len(keyword_lower), len(word_in_cv))
                    if len_max > 0:
                        distance = levenshtein_distance(keyword_lower, word_in_cv)
                        similarity = (1 - (distance / len_max)) * 100
                        if SIMILARITY_THRESHOLD <= similarity < 100:
                            fuzzy_key = f"{word_in_cv} (~)"
                            fuzzy_matches[fuzzy_key] = fuzzy_matches.get(fuzzy_key, 0) + 1

            if fuzzy_matches:
                fuzzy_results_map[applicant_id] = ApplicantMatchData(
                    detail_id=int(applicant_id),
                    name=f"Applicant {applicant_id}",
                    match_count=sum(fuzzy_matches.values()),
                    matched_keywords=fuzzy_matches,
                )
        
        end_time_fuzzy = time.time()
        runtime_ms_fuzzy = (end_time_fuzzy - start_time) * 1000
        print(f"Search complete in {runtime_ms_fuzzy:.2f} ms. Found {len(fuzzy_results_map)} matching applicants (Fuzzy).")
        
        sorted_results_fuzzy = sorted(fuzzy_results_map.values(), key=lambda x: x.match_count, reverse=True)
        top_results_fuzzy = sorted_results_fuzzy[:search_params.top_matches]
        self.search_page.result_display.set_results(SearchResult(
            applicants=top_results_fuzzy,
            cvs_scanned=len(all_files),
            runtime=runtime_ms_fuzzy
        ), is_fuzzy=True)

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

    def summary(self, detail_id: str):
        """
        Retrieves the summary (full text content) for the given detail_id,
        updates the summary page, and switches the view.
        """
        print(f"Viewing summary for applicant ID: {detail_id}")
        
        applicant_data = None
        if self.db:
            applicant_data = self.db.get_applicant_data(detail_id)
        
        if applicant_data:
            # TO DO: Implement the logic to extract and display the summary
            pass