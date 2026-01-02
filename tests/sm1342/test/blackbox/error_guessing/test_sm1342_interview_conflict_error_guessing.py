import pytest
from src.services.job_service import JobService
from src.services.candidate_service import CandidateService
from src.services.application_service import ApplicationService
from src.services.interview_service import InterviewService
from src.app.exceptions import ConflictError

from tests._helpers import make_repo

def setup_shortlisted_app(repo, app_id, cand_id, email):
    JobService(repo).create_job_posting(
        job_id="JOB001", title="SE", location="London", job_type="full_time",
        min_salary=30000, max_salary=50000, required_skills=["python"], min_experience_years=0, visa_required=False
    )
    CandidateService(repo).create_candidate_profile(
        candidate_id=cand_id, name="A", email=email, phone="+447700900123",
        location="London", years_experience=1, skills=["python"], education_level="bachelors", visa_status="no_sponsorship"
    )
    ApplicationService(repo).submit_application(app_id, "JOB001", cand_id)
    ApplicationService(repo).update_application_status(app_id, "screened", "ok")
    ApplicationService(repo).update_application_status(app_id, "shortlisted", "ok")

def test_interviewer_double_booking_conflict(tmp_path):
    repo = make_repo(tmp_path)

    setup_shortlisted_app(repo, "APP001", "CAND001", "a1@example.com")
    setup_shortlisted_app(repo, "APP002", "CAND002", "a2@example.com")

    svc = InterviewService(repo)
    svc.schedule_interview("INT001", "APP001", "2025-12-20T10:00:00", 60, "interviewer1", "online")

    with pytest.raises(ConflictError):
        svc.schedule_interview("INT002", "APP002", "2025-12-20T10:30:00", 60, "interviewer1", "online")
