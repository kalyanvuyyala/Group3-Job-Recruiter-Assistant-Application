import pytest
from src.services.job_service import JobService
from src.services.candidate_service import CandidateService
from src.services.application_service import ApplicationService
from src.app.exceptions import NotFoundError, ConflictError

from tests._helpers import make_repo

def setup_job_and_candidate(repo):
    JobService(repo).create_job_posting(
        job_id="JOB001", title="SE", location="London", job_type="full_time",
        min_salary=30000, max_salary=50000, required_skills=["python"], min_experience_years=0, visa_required=False
    )
    CandidateService(repo).create_candidate_profile(
        candidate_id="CAND001", name="A", email="a@example.com", phone="+447700900123",
        location="London", years_experience=1, skills=["python"], education_level="bachelors", visa_status="no_sponsorship"
    )

def test_submit_application_valid(tmp_path):
    repo = make_repo(tmp_path)
    setup_job_and_candidate(repo)
    svc = ApplicationService(repo)

    app = svc.submit_application("APP001", "JOB001", "CAND001")
    assert app["status"] == "applied"

def test_submit_application_job_missing(tmp_path):
    repo = make_repo(tmp_path)
    CandidateService(repo).create_candidate_profile(
        candidate_id="CAND001", name="A", email="a@example.com", phone="+447700900123",
        location="London", years_experience=1, skills=["python"], education_level="bachelors", visa_status="no_sponsorship"
    )
    svc = ApplicationService(repo)

    with pytest.raises(NotFoundError):
        svc.submit_application("APP001", "JOB404", "CAND001")

def test_submit_application_duplicate_same_job_same_candidate(tmp_path):
    repo = make_repo(tmp_path)
    setup_job_and_candidate(repo)
    svc = ApplicationService(repo)

    svc.submit_application("APP001", "JOB001", "CAND001")
    with pytest.raises(ConflictError):
        svc.submit_application("APP002", "JOB001", "CAND001")
