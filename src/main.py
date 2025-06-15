import sys
import traceback
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

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
    main()