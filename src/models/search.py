from dataclasses import dataclass
from enum import Enum
from datetime import datetime

""" Database models """ 
@dataclass
class ApplicantProfile:
    applicant_id: int
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    phone_number: str

@dataclass
class ApplicationDetail:
    detail_id: int
    applicant_id: int
    application_role: str
    cv_path: str

""" Search data """
class SearchAlgorithm(Enum):
    KMP = "KMP"
    BM = "BM"
    AHO_CORASICK = "Aho-Corasick"

@dataclass
class ApplicantMatchData:
    detail_id: int
    name: str
    match_count: int
    matched_keywords: dict[str, int]

@dataclass
class SearchResult:
    applicants: list[ApplicantMatchData]
    cvs_scanned: int
    runtime: float  # In milliseconds

@dataclass
class SearchParams:
    keywords: list[str]
    algorithm: SearchAlgorithm
    top_matches: int

# Summary data
@dataclass
class EducationEntry:
    institution: str
    program: str
    start_date: str
    end_date: str

@dataclass
class WorkExperienceEntry:
    position: str
    company: str
    start_date: str
    end_date: str
    description: str

@dataclass
class CVSummary:
    name: str
    birthdate: datetime
    address: str
    contacts: list[str] # Phone, emails, etc
    description: str

    skills: list[str]
    education: list[EducationEntry]
    work_experience: list[WorkExperienceEntry]

"""CV Extraction data"""
@dataclass
class CVPersonalData:
    # Database
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    phone_number: str

@dataclass
class CVSummaryExtraction:
    # Extracted at runtime
    description: str
    skills: list[str]
    education: list[EducationEntry]
    work_experience: list[WorkExperienceEntry]