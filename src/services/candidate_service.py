from typing import Dict, Any, List
from src.app.exceptions import ValidationError, NotFoundError
from src.app.utils import ensure_non_empty, validate_email, validate_phone, normalise_text, normalise_skills
from src.domain.models import CandidateProfile
from src.storage.repository import Repository

class CandidateService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def create_candidate_profile(self, candidate_id: str, name: str, email: str, phone: str,
                                 location: str, years_experience: int, skills: List[str],
                                 education_level: str, visa_status: str) -> Dict[str, Any]:
        db = self.repo.load()
        ensure_non_empty("candidate_id", candidate_id)
        ensure_non_empty("name", name)
        validate_email(email)
        validate_phone(phone)
        ensure_non_empty("location", location)
        if years_experience < 0:
            raise ValidationError("years_experience cannot be negative.")

        cid = normalise_text(candidate_id)
        if cid in db["candidates"]:
            raise ValidationError("Candidate ID already exists.")
        email_norm = normalise_text(email)
        for c in db["candidates"].values():
            if normalise_text(c["email"]) == email_norm:
                raise ValidationError("Email already exists.")

        profile = CandidateProfile(
            candidate_id=cid,
            name=" ".join(name.strip().split()),
            email=email.strip(),
            phone=phone.strip(),
            location=" ".join(location.strip().split()),
            years_experience=int(years_experience),
            skills=normalise_skills(skills),
            education_level=normalise_text(education_level or "unknown"),
            visa_status=normalise_text(visa_status or "unknown"),
        )
        db["candidates"][cid] = profile.to_dict()
        self.repo.save(db)
        return profile.to_dict()

    def update_candidate_profile(self, candidate_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        db = self.repo.load()
        cid = normalise_text(candidate_id)
        prof = db["candidates"].get(cid)
        if not prof:
            raise NotFoundError("Candidate not found.")

        allowed = {"name", "email", "phone", "location", "years_experience",
                   "skills", "education_level", "visa_status"}
        for k in updates.keys():
            if k not in allowed:
                raise ValidationError(f"Field not editable: {k}")

        if "name" in updates:
            ensure_non_empty("name", updates["name"])
            prof["name"] = " ".join(str(updates["name"]).strip().split())

        if "email" in updates:
            validate_email(str(updates["email"]))
            email_norm = normalise_text(str(updates["email"]))
            for other_id, c in db["candidates"].items():
                if other_id != cid and normalise_text(c["email"]) == email_norm:
                    raise ValidationError("Email already exists.")
            prof["email"] = str(updates["email"]).strip()

        if "phone" in updates:
            validate_phone(str(updates["phone"]))
            prof["phone"] = str(updates["phone"]).strip()

        if "location" in updates:
            ensure_non_empty("location", updates["location"])
            prof["location"] = " ".join(str(updates["location"]).strip().split())

        if "years_experience" in updates:
            ye = int(updates["years_experience"])
            if ye < 0:
                raise ValidationError("years_experience cannot be negative.")
            prof["years_experience"] = ye

        if "skills" in updates:
            prof["skills"] = normalise_skills(list(updates["skills"]))

        if "education_level" in updates:
            prof["education_level"] = normalise_text(str(updates["education_level"]))

        if "visa_status" in updates:
            prof["visa_status"] = normalise_text(str(updates["visa_status"]))

        db["candidates"][cid] = prof
        self.repo.save(db)
        return prof

    def view_candidate_profile(self, candidate_id: str) -> Dict[str, Any]:
        db = self.repo.load()
        cid = normalise_text(candidate_id)
        prof = db["candidates"].get(cid)
        if not prof:
            raise NotFoundError("Candidate not found.")
        return prof
