from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class JobPosting:
    job_id: str
    title: str
    location: str
    job_type: str
    min_salary: int
    max_salary: int
    required_skills: List[str] = field(default_factory=list)
    min_experience_years: int = 0
    visa_required: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class CandidateProfile:
    candidate_id: str
    name: str
    email: str
    phone: str
    location: str
    years_experience: int
    skills: List[str] = field(default_factory=list)
    education_level: str = "unknown"
    visa_status: str = "unknown"
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Application:
    application_id: str
    job_id: str
    candidate_id: str
    status: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    audit_trail: List[Dict] = field(default_factory=list)

    def add_audit(self, action: str, details: Optional[Dict] = None) -> None:
        self.audit_trail.append(
            {"ts": datetime.utcnow().isoformat(), "action": action, "details": details or {}}
        )
        self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Interview:
    interview_id: str
    application_id: str
    scheduled_time: str
    duration_minutes: int
    interviewer: str
    location: str = "online"
    cancelled: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)
