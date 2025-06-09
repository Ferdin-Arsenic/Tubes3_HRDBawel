import sys
from gui.app import App

def main():
    print("Hello from tubes3-hrdbawel!")

    app = App(argv=sys.argv)
    app.root.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
