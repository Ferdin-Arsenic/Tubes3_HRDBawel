from dataclasses import dataclass
from enum import Enum

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
    runtime: float

@dataclass
class SearchParams:
    keywords: list[str]
    algorithm: SearchAlgorithm
    top_matches: int