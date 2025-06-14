from PyQt6.QtWidgets import QMainWindow, QStackedWidget
import time
import os
import re
from gui.search_page import SearchPage
from gui.summary_page import SummaryPage
from models.search import SearchParams, ApplicantMatchData, SearchResult
from models.search import SearchAlgorithm 

#from database.cv_database import DBConnection 
from lib.kmp import KMP
from lib.bm import BM
from lib.aho_corasick import aho_corasick
from lib.levenshtein import levenshtein_distance

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
        if not search_function:
            print(f"Error: Algorithm {search_params.algorithm} not found.")
            return
            
        print(f"[DEBUG] Using algorithm: {search_params.algorithm.name}")

        base_dir = os.path.dirname(os.path.dirname(__file__))
        text_files_dir = os.path.join(base_dir, "dataset", "txt")
        if not os.path.isdir(text_files_dir):
            print(f"Error: Directory not found at {text_files_dir}")
            return
            
        all_files = [f for f in os.listdir(text_files_dir) if f.endswith(".txt")]
        final_results_map = {}

        # TAHAP 1: PENCARIAN EXACT MATCH
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

        # TAHAP 2: PROSES HASIL
        if final_results_map:
            end_time = time.time()
            runtime_ms = (end_time - start_time) * 1000
            print(f"Search complete in {runtime_ms:.2f} ms. Found {len(final_results_map)} matching applicants (Exact).")
            
            sorted_results = sorted(final_results_map.values(), key=lambda x: x.match_count, reverse=True)
            top_results = sorted_results[:search_params.top_matches]
            self.search_page.result_display.set_results(top_results, runtime_ms, 0, is_fuzzy=False)
            return

        # JIKA TIDAK ADA EXACT MATCH, JALANKAN FUZZY SEARCH
        print("[DEBUG] No exact matches found. Falling back to fuzzy search.")
        SIMILARITY_THRESHOLD = 80.0
        fuzzy_results_map = {}

        for filename in all_files:
            applicant_id = os.path.splitext(filename)[0]
            file_path = os.path.join(text_files_dir, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    # --- PERBAIKAN DI SINI ---
                    # Membersihkan teks dari tanda baca untuk mendapatkan kata-kata murni
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
        self.search_page.result_display.set_results(top_results_fuzzy, 0, runtime_ms_fuzzy, is_fuzzy=True)

    def view_cv(self, detail_id: id):
        print(f"Viewing CV for applicant ID: {detail_id}")
        # Show CV pdf

    def summary(self, detail_id: id):
        print(f"Viewing summary for applicant ID: {detail_id}")
        # Extracted CV summary
