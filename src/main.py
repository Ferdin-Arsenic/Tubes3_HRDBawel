import sys
import traceback
import argparse
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from database.cv_database import CVDatabase

def main():
    try:
        print("Hello from tubes3-hrdbawel!")
        print("Initializing QApplication...")
        
        app = QApplication(sys.argv)
        print("QApplication created successfully")
        
        print("Creating MainWindow...")
        try:
            window = MainWindow()
            print("MainWindow created successfully")
        except Exception as e:
            print(f"Error creating MainWindow: {e}")
            traceback.print_exc()
            return
        
        print("Showing window...")
        window.show()
        print("Window shown successfully")
        
        print("Starting event loop...")
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure all required modules are available")
        traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
    
    input("Press Enter to continue...")  # Pause untuk melihat error

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool to analyze and search through CVs.")
    parser.add_argument("--seed",
                        nargs='+',
                        metavar=('PATH', '[ROLE]'),
                        help="Populate the database with CVs from PATH, filled in with the specified ROLE.")

    args = parser.parse_args()
    if args.seed:
        database = CVDatabase()
        relative_path = args.seed[0].replace("/", "\\")
        role = args.seed[1] if len(args.seed) > 1 else None
        if role:
            database.seed_database(relative_path, role)
        else:
            database.seed_database(relative_path)
    else:
        main()