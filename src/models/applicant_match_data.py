from dataclasses import dataclass

@dataclass
class ApplicantMatchData:
    detail_id: int
    name: str
    match_count: int
    matched_keywords: dict[str, int]