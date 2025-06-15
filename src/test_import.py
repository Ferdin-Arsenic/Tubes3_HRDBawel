"""
Simple test to check which imports are failing
"""

def test_imports():
    print("Testing imports...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
        print("✓ PyQt6.QtWidgets OK")
    except Exception as e:
        print(f"✗ PyQt6.QtWidgets FAILED: {e}")
        return False
    
    try:
        from gui.search_page import SearchPage
        print("✓ gui.search_page OK")
    except Exception as e:
        print(f"✗ gui.search_page FAILED: {e}")
        return False
    
    try:
        from gui.summary_page import SummaryPage
        print("✓ gui.summary_page OK")
    except Exception as e:
        print(f"✗ gui.summary_page FAILED: {e}")
        return False
    
    try:
        from models.search import SearchParams, ApplicantMatchData, SearchAlgorithm
        print("✓ models.search OK")
    except Exception as e:
        print(f"✗ models.search FAILED: {e}")
        return False
    
    try:
        from lib.kmp import KMP
        from lib.bm import BM
        from lib.aho_corasick import aho_corasick
        from lib.levenshtein import levenshtein_distance
        print("✓ lib modules OK")
    except Exception as e:
        print(f"✗ lib modules FAILED: {e}")
        return False
    
    try:
        from database.cv_database import CvDatabase
        print("✓ database.cv_database OK")
    except Exception as e:
        print(f"✗ database.cv_database FAILED: {e}")
        return False
    
    print("All imports successful!")
    return True

if __name__ == "__main__":
    import sys
    import os
    
    # Add src directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    if test_imports():
        print("\nTrying to create CvDatabase...")
        try:
            from database.cv_database import CvDatabase
            db = CvDatabase()
            print("✓ CvDatabase created successfully")
        except Exception as e:
            print(f"✗ CvDatabase creation failed: {e}")
            import traceback
            traceback.print_exc()
    
    input("Press Enter to exit...")