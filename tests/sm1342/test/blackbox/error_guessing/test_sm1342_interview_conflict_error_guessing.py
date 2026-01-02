import pytest
from src.services.job_service import JobService
from src.services.candidate_service import CandidateService
from src.services.application_service import ApplicationService
from src.services.interview_service import InterviewService
from src.app.exceptions import ConflictError

from tests._helpers import make_repo

def setup_shortlisted_application(repo):
    JobService(repo).create_job_posting(
        job_id="JOB001", title="SE", location="London", job_type="full_time",
        min_salary=30000, max_salary=50000, required_skills=["python"], min_experience_years=0, visa_required=False
    )
    CandidateService(repo).create_candidate_profile(
        candidate_id="CAND001", name="A", email="a@example.com", phone="+447700900123",
        location="London", years_experience=1, skills=["python"], education_level="bachelors", visa_status="no_sponsorship"
    )
    app = ApplicationService(repo).submit_application("APP001", "JOB001", "CAND001")
    # move to shortlisted (required for scheduling)
    ApplicationService(repo).update_application_status("APP001", "screened", "ok")
    ApplicationService(repo).update_application_status("APP001", "shortlisted", "ok")
    return app

def test_interviewer_double_booking_conflict(tmp_path):
    repo = make_repo(tmp_path)
    setup_shortlisted_application(repo)
    svc = InterviewService(repo)

    svc.schedule_interview("INT001", "APP001", "2025-12-20T10:00:00", 60, "interviewer1", "online")

    # overlapping time should fail
    with pytest.raises(ConflictError):
        svc.schedule_interview("INT002", "APP001", "2025-12-20T10:30:00", 60, "interviewer1", "online")
