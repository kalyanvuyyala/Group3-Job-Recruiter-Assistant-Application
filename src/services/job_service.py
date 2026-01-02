from typing import Dict, Any, List
from src.app.exceptions import ValidationError, NotFoundError
from src.app.utils import ensure_non_empty, validate_salary, ensure_unique_id, normalise_text, normalise_skills
from src.domain.models import JobPosting
from src.storage.repository import Repository

class JobService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def create_job_posting(self, job_id: str, title: str, location: str, job_type: str,
                           min_salary: int, max_salary: int, required_skills: List[str],
                           min_experience_years: int, visa_required: bool) -> Dict[str, Any]:
        db = self.repo.load()
        ensure_non_empty("job_id", job_id)
        ensure_non_empty("title", title)
        ensure_non_empty("location", location)
        ensure_non_empty("job_type", job_type)
        validate_salary(min_salary, max_salary)
        if min_experience_years < 0:
            raise ValidationError("Experience years cannot be negative.")

        job_id_norm = normalise_text(job_id)
        ensure_unique_id(db["jobs"], job_id_norm, "Job")

        job = JobPosting(
            job_id=job_id_norm,
            title=" ".join(title.strip().split()),
            location=" ".join(location.strip().split()),
            job_type=normalise_text(job_type),
            min_salary=int(min_salary),
            max_salary=int(max_salary),
            required_skills=normalise_skills(required_skills),
            min_experience_years=int(min_experience_years),
            visa_required=bool(visa_required),
        )
        db["jobs"][job.job_id] = job.to_dict()
        self.repo.save(db)
        return job.to_dict()

    def edit_job_posting(self, job_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        db = self.repo.load()
        job_id_norm = normalise_text(job_id)
        job = db["jobs"].get(job_id_norm)
        if not job:
            raise NotFoundError("Job not found.")

        allowed = {"title", "location", "job_type", "min_salary", "max_salary",
                   "required_skills", "min_experience_years", "visa_required"}
        for k in updates.keys():
            if k not in allowed:
                raise ValidationError(f"Field not editable: {k}")

        if "title" in updates:
            ensure_non_empty("title", updates["title"])
            job["title"] = " ".join(str(updates["title"]).strip().split())

        if "location" in updates:
            ensure_non_empty("location", updates["location"])
            job["location"] = " ".join(str(updates["location"]).strip().split())

        if "job_type" in updates:
            ensure_non_empty("job_type", updates["job_type"])
            job["job_type"] = normalise_text(str(updates["job_type"]))

        if "required_skills" in updates:
            job["required_skills"] = normalise_skills(list(updates["required_skills"]))

        min_salary = int(updates.get("min_salary", job["min_salary"]))
        max_salary = int(updates.get("max_salary", job["max_salary"]))
        validate_salary(min_salary, max_salary)
        job["min_salary"] = min_salary
        job["max_salary"] = max_salary

        if "min_experience_years" in updates:
            exp = int(updates["min_experience_years"])
            if exp < 0:
                raise ValidationError("Experience years cannot be negative.")
            job["min_experience_years"] = exp

        if "visa_required" in updates:
            job["visa_required"] = bool(updates["visa_required"])

        db["jobs"][job_id_norm] = job
        self.repo.save(db)
        return job

    def search_jobs(self, keyword: str = "", location: str = "", job_type: str = "") -> List[Dict[str, Any]]:
        db = self.repo.load()
        k = normalise_text(keyword)
        loc = normalise_text(location)
        jt = normalise_text(job_type)

        results = []
        for job in db["jobs"].values():
            title_match = (not k) or (k in normalise_text(job["title"]))
            loc_match = (not loc) or (loc in normalise_text(job["location"]))
            type_match = (not jt) or (jt == normalise_text(job["job_type"]))
            if title_match and loc_match and type_match:
                results.append(job)

        results.sort(key=lambda j: (normalise_text(j["title"]), normalise_text(j["location"])))
        return results
