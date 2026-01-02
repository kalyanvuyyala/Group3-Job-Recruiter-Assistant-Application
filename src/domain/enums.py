from enum import Enum

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SCREENED = "screened"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    INTERVIEW_SCHEDULED = "interview_scheduled"
