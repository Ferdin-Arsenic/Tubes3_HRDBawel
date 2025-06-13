from PyQt6.QtWidgets import QMainWindow, QStackedWidget
import time
from gui.search_page import SearchPage
from gui.summary_page import SummaryPage
from models.search import SearchParams, ApplicantMatchData

#from database.cv_database import DBConnection 
#from lib.kmp import KMP
from lib.bm import BM
#from lib.aho_corasick import aho_corasick
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
        """
        Metode utama untuk menjalankan proses pencarian dua tahap.
        """
        print("Search initiated with parameters:", search_params)
        
        # Dummy
        all_cv_texts = {
            1: "John Doe. Experience in Python, Java, and SQL.",
            2: "Jane Smith. Skilled in React, Node.js, SQL, and MongoDB.",
            3: "Peter Jones. Proficient in C++ and Python programming.",
            4: "Richard Roe. Knows reactt and is a SQL expert.",
        }
        start_time_exact = time.time()
        
        exact_match_results = {} 
        found_keywords = set()

        search_function = BM # Ganti berdasarkan pilihan pengguna (BM atau Aho-C)

        for cv_id, cv_text in all_cv_texts.items():
            for keyword in search_params.keywords:
                matches = search_function(cv_text.lower(), keyword.lower())
                if matches:
                    found_keywords.add(keyword)
                    if cv_id not in exact_match_results:
                        exact_match_results[cv_id] = {"name": f"Applicant {cv_id}", "matches": {}}
                    exact_match_results[cv_id]["matches"][keyword] = len(matches)

        end_time_exact = time.time()
        execution_time_exact = end_time_exact - start_time_exact
        
        fuzzy_match_results = {}
        execution_time_fuzzy = 0
        keywords_for_fuzzy = [kw for kw in search_params.keywords if kw not in found_keywords]

        if keywords_for_fuzzy:
            start_time_fuzzy = time.perf_counter()
            for cv_id, cv_text in all_cv_texts.items():
                cv_words = set(cv_text.lower().replace('.', '').replace(',', '').split())
                for keyword in keywords_for_fuzzy:
                    for word in cv_words:
                        distance = levenshtein_distance(keyword.lower(), word)
                        if distance > 0 and distance <= 2: #threshold for fuzzy match
                            if cv_id not in fuzzy_match_results:
                                fuzzy_match_results[cv_id] = {"name": f"Applicant {cv_id}", "matches": {}}
                            
                            len_max = max(len(keyword), len(word))
                            if len_max > 0:
                                similarity_percent = (1 - (distance / len_max)) * 100
                            else:
                                similarity_percent = 100

                            fuzzy_keyword = f"{keyword} ({similarity_percent:.0f}%)"
                            
                            fuzzy_match_results[cv_id]["matches"][fuzzy_keyword] = 1

            end_time_fuzzy = time.perf_counter()
            execution_time_fuzzy = (end_time_fuzzy - start_time_fuzzy) * 1000 # ms

        final_results_map = {}
        for cv_id, data in exact_match_results.items():
            final_results_map[cv_id] = data
        
        for cv_id, data in fuzzy_match_results.items():
            if cv_id not in final_results_map:
                final_results_map[cv_id] = data
            else:
                final_results_map[cv_id]["matches"].update(data["matches"])

        formatted_results = []
        for cv_id, data in final_results_map.items():
            formatted_results.append(
                ApplicantMatchData(
                    detail_id=cv_id,
                    name=data["name"],
                    match_count=len(data["matches"]),
                    matched_keywords=data["matches"]
                )
            )
        
        formatted_results.sort(key=lambda x: x.match_count, reverse=True)

        self.search_page.result_display.set_results(
            results=formatted_results,
            exact_time=execution_time_exact,
            fuzzy_time=execution_time_fuzzy
        )
        # Compute

    def view_cv(self, detail_id: id):
        print(f"Viewing CV for applicant ID: {detail_id}")
        # Show CV pdf

    def summary(self, detail_id: id):
        print(f"Viewing summary for applicant ID: {detail_id}")
        # Extracted CV summary
