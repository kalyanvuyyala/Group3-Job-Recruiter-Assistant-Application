import pytest
from src.services.job_service import JobService
from src.app.exceptions import ValidationError

from tests._helpers import make_repo

def test_create_job_valid_equivalence(tmp_path):
    repo = make_repo(tmp_path)
    svc = JobService(repo)

    job = svc.create_job_posting(
        job_id="JOB001",
        title="Data Engineer",
        location="Leicester",
        job_type="full_time",
        min_salary=35000,
        max_salary=55000,
        required_skills=["python", "sql", "spark"],
        min_experience_years=1,
        visa_required=False
    )
    assert job["job_id"] == "job001"

def test_create_job_invalid_salary_equivalence(tmp_path):
    repo = make_repo(tmp_path)
    svc = JobService(repo)

    with pytest.raises(ValidationError):
        svc.create_job_posting(
            job_id="JOB002",
            title="Role",
            location="London",
            job_type="full_time",
            min_salary=60000,
            max_salary=50000,
            required_skills=["python"],
            min_experience_years=0,
            visa_required=False
        )
