from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QScrollArea,QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from models.search import CVSummary
from gui.wrap import HorizontalWrapGroup

class SummaryPage(QWidget):
    return_from_summary = pyqtSignal()  # Signal to return to search page

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #d9d9d9; color: #000000;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        main_layout.addWidget(scroll_area)
        
        self.container = QWidget()
        scroll_area.setWidget(self.container)
        
        self.detail_id = -1 # If displaying this page and the detail_id differs, the page will update

        self.initialize_widgets()


    """ Page Builder """
    def initialize_widgets(self) -> None:
        summary_page_layout = QGridLayout(self.container)
        summary_page_layout.setContentsMargins(20, 20, 20, 20)
        summary_page_layout.setSpacing(0)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(5, 5, 5, 5)
        title_layout.setSpacing(10)
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(5, 5, 5, 5)
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setContentsMargins(5, 5, 5, 5)
        right_panel_layout.setSpacing(10)
        summary_page_layout.addLayout(title_layout, 0, 0, 1, 2)
        summary_page_layout.addLayout(left_panel_layout, 1, 0)
        summary_page_layout.addLayout(right_panel_layout, 1, 1)

        self.main_info_card = BlankCard(width=290)
        self.job_history_card = BlankCard(width=290)
        self.education_card = BlankCard(width=290)

        left_panel_layout.addWidget(self.main_info_card)
        left_panel_layout.addStretch(1)
        right_panel_layout.addWidget(self.job_history_card)
        right_panel_layout.addWidget(self.education_card)
        right_panel_layout.addStretch(1)

        self.initialize_widgets_title(title_layout)
        self.initialize_widgets_main_info(self.main_info_card.get_layout())
        self.initialize_widgets_job_history(self.job_history_card.get_layout())
        self.initialize_widgets_education(self.education_card.get_layout())        
    
    def initialize_widgets_title(self, layout) -> None:
        back_button = QPushButton("<", clicked=self.return_from_summary.emit)
        back_button.setFixedSize(25, 25)
        back_button.setStyleSheet("font-size: 14px; font-family: Inter, sans-serif; border-radius: 12px; background-color: #C9F5A2; color: #000000; font-weight: bold;")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        title_label = QLabel("Showing CV Summary")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Inter, sans-serif; color: #000000;")
        
        layout.addWidget(back_button, alignment = Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(title_label, alignment = Qt.AlignmentFlag.AlignVCenter)

    def initialize_widgets_main_info(self, layout) -> None:
        self.name_label = QLabel("Nama Pertama")
        self.name_label.setStyleSheet("font-size: 20px; font-weight: bold; font-family: Inter, sans-serif; color: #000000;")
        layout.addWidget(self.name_label)

        self.birthdate_label = QLabel("Date of Birth: 01 February 1990")
        self.birthdate_label.setStyleSheet("font-size: 10px; font-family: Inter, sans-serif; color: #9a9a9a;")
        self.birthdate_label.setFixedHeight(10)
        layout.addWidget(self.birthdate_label)
        self.address_label = QLabel("Address: 123 Main St, City, Country")
        self.address_label.setStyleSheet("font-size: 10px; font-family: Inter, sans-serif; color: #9a9a9a;")
        self.address_label.setFixedHeight(10)
        layout.addWidget(self.address_label)
        self.contacts_label = QLabel("Contact: +6281234567890 | email@abc.xyz")
        self.contacts_label.setStyleSheet("font-size: 10px; font-family: Inter, sans-serif; color: #9a9a9a;")
        self.contacts_label.setFixedHeight(10)
        layout.addWidget(self.contacts_label)

        self.description_label = QLabel("Description: A brief summary of the applicant's qualifications and experience.")
        self.description_label.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; color: #000000; padding: 10px 0px 10px 0px;")
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        self.skills_label = QLabel("Skills")
        self.skills_label.setStyleSheet("font-size: 12px; font-weight: bold; font-family: Inter, sans-serif; color: #000000;")
        layout.addWidget(self.skills_label)

        self.skills_group = HorizontalWrapGroup(width=270)
        layout.addWidget(self.skills_group)

    def initialize_widgets_job_history(self, layout) -> None:
        job_history_label = QLabel("Job History")
        job_history_label.setStyleSheet("font-size: 12px; font-weight: bold; font-family: Inter, sans-serif; color: #000000;")
        layout.addWidget(job_history_label)
        
        self.job_histories_layout = QVBoxLayout()
        self.job_histories_layout.setContentsMargins(0, 10, 0, 10)
        self.job_histories_layout.setSpacing(10)
        layout.addLayout(self.job_histories_layout)

        # Placeholder for job history content        
        self.job_histories_layout.addWidget(EntryItem("Company ABC", "Software Engineer | 2015-2020"))
        self.job_histories_layout.addWidget(EntryItem("Company XYZ", "Senior Developer | 2020-2023"))

    def initialize_widgets_education(self, layout) -> None:
        education_header = QLabel("Education")
        education_header.setStyleSheet("font-size: 12px; font-weight: bold; font-family: Inter, sans-serif; color: #000000;")
        layout.addWidget(education_header)

        self.educations_layout = QVBoxLayout()
        self.educations_layout.setContentsMargins(0, 0, 0, 0)
        self.educations_layout.setSpacing(10)
        layout.addLayout(self.educations_layout)

        # Placeholder
        education_label = EntryItem("University XYZ", "Bachelor of Science in Computer Science | 2010-2014")
        self.educations_layout.addWidget(education_label)

    
    """ Controls """
    def set_summary(self, detail_id: int, summary: CVSummary) -> None:
        if detail_id == self.detail_id:
            return
        self.detail_id = detail_id
        
        self.name_label.setText(summary.name)
        self.birthdate_label.setText(f"Date of Birth: {summary.birthdate.strftime("%d %B %Y")}")
        self.address_label.setText(f"Address: {summary.address}")
        self.contacts_label.setText(f"Contact: {', '.join(summary.contacts)}")

        self.description_label.setText(summary.description)
        self.skills_group.set_widgets([PillLabel(skill) for skill in summary.skills])

        while self.job_histories_layout.count():
            item = self.job_histories_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for job in summary.work_experience:
            duration = f' | {job.start_date if job.start_date else ""} - {job.end_date if job.end_date else ""}' if job.start_date or job.end_date else ""
            desc = f"\n{job.description}" if job.description else ""
            entry = EntryItem(job.position, f"{job.company}{duration}{desc}")
            self.job_histories_layout.addWidget(entry)
        while self.educations_layout.count():
            item = self.educations_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for edu in summary.education:
            duration = f' | {edu.start_date if edu.start_date else ""} - {edu.end_date if edu.end_date else ""}' if edu.start_date or edu.end_date else ""
            entry = EntryItem(edu.institution, f"{edu.program}{duration}")
            self.educations_layout.addWidget(entry)



class PillLabel(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        padding = 10
        font_metrics = self.fontMetrics()
        text_width = font_metrics.horizontalAdvance(text)
        total_width = (padding * 2) + text_width
        self.setStyleSheet("font-size: 12px; font-family: Inter, sans-serif; border-radius: 10px; background-color: #C9F5A2; color: #000000;")
        self.setFixedHeight(20)
        self.setFixedWidth(total_width)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class EntryItem(QWidget):
    def __init__(self, main_label, sublabel, parent=None):
        super().__init__(parent)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        bullet = QWidget()
        bullet.setFixedSize(5, 5)
        bullet.setStyleSheet("background-color: #ccff79; border-radius: 2px;")
        main_layout.addWidget(bullet)

        label_layout = QVBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(0)
        main_layout.addLayout(label_layout, 1)

        main_label_widget = QLabel(main_label)
        main_label_widget.setStyleSheet("font-size: 12px; font-weight: bold; font-family: Inter, sans-serif; color: #000000;")
        main_label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_label_widget.setWordWrap(True)
        label_layout.addWidget(main_label_widget)
        sublabel_widget = QLabel(sublabel)
        sublabel_widget.setStyleSheet("font-size: 10px; font-family: Inter, sans-serif; color: #9a9a9a;")
        sublabel_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sublabel_widget.setWordWrap(True)
        label_layout.addWidget(sublabel_widget)

class BlankCard(QWidget):
    def __init__(self, width=-1, height=-1, parent=None):
        super().__init__(parent)
        if width > 0:
            self.setFixedWidth(width)
        if height > 0:
            self.setFixedHeight(height)
        self.setStyleSheet("background-color: #ffffff; border-radius: 10px;")
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container = QWidget()
        container_layout.addWidget(container)
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
    
    def get_layout(self) -> QVBoxLayout:
        return self.main_layout
