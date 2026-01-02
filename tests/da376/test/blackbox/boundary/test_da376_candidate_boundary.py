import pytest
from src.services.candidate_service import CandidateService
from src.app.exceptions import ValidationError

from tests._helpers import make_repo

def test_candidate_years_experience_boundary_zero(tmp_path):
    repo = make_repo(tmp_path)
    svc = CandidateService(repo)

    c = svc.create_candidate_profile(
        candidate_id="CAND001",
        name="Candidate One",
        email="candidate1@example.com",
        phone="+447700900111",
        location="Leicester",
        years_experience=0,
        skills=["python", "sql"],
        education_level="masters",
        visa_status="needs_sponsorship"
    )
    assert c["years_experience"] == 0

def test_candidate_years_experience_negative_invalid(tmp_path):
    repo = make_repo(tmp_path)
    svc = CandidateService(repo)

    with pytest.raises(ValidationError):
        svc.create_candidate_profile(
            candidate_id="CAND002",
            name="Candidate Two",
            email="candidate2@example.com",
            phone="+447700900112",
            location="London",
            years_experience=-1,
            skills=["python"],
            education_level="bachelors",
            visa_status="no_sponsorship"
        )
