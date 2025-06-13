import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    print("Hello from tubes3-hrdbawel!")

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

    # import sys
    # from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout
    # from gui.applicant_card import ApplicantCard
    # from models.applicant_match_data import ApplicantMatchData

    # app = QApplication(sys.argv)
    # frame = QFrame()
    # frame.setStyleSheet("background-color: #ff0000;")
    # frame.setFixedSize(400, 400)
    # layout = QVBoxLayout(frame)
    # frame.setLayout(layout)
    # frame.show()

    # data = ApplicantMatchData(
    #     detail_id=1,
    #     name="John Doe",
    #     match_count=5,
    #     matched_keywords={"Python": 3, "Java": 2, "C++": 1, "SQL": 4, "JavaScript": 2}
    # )
    # card = ApplicantCard(data)
    # card.view_summary.connect(lambda id: print(f"View summary for ID: {id}"))
    # card.view_cv.connect(lambda id: print(f"View CV for ID: {id}"))
    # layout.addWidget(card)
    # sys.exit(app.exec())
