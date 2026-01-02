from typing import Dict, Any, List
from datetime import datetime
from src.app.exceptions import ValidationError, NotFoundError, ConflictError, StateError
from src.app.utils import ensure_non_empty, normalise_text
from src.domain.enums import ApplicationStatus
from src.domain.models import Application
from src.storage.repository import Repository

class ApplicationService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def submit_application(self, application_id: str, job_id: str, candidate_id: str) -> Dict[str, Any]:
        db = self.repo.load()
        ensure_non_empty("application_id", application_id)
        jid = normalise_text(job_id)
        cid = normalise_text(candidate_id)
        aid = normalise_text(application_id)

        if jid not in db["jobs"]:
            raise NotFoundError("Job not found.")
        if cid not in db["candidates"]:
            raise NotFoundError("Candidate not found.")
        if aid in db["applications"]:
            raise ValidationError("Application ID already exists.")

        for a in db["applications"].values():
            if a["job_id"] == jid and a["candidate_id"] == cid and a["status"] != ApplicationStatus.WITHDRAWN.value:
                raise ConflictError("Duplicate application for same job and candidate.")

        app = Application(
            application_id=aid,
            job_id=jid,
            candidate_id=cid,
            status=ApplicationStatus.APPLIED.value
        )
        app.add_audit("created", {"job_id": jid, "candidate_id": cid})
        db["applications"][aid] = app.to_dict()
        self.repo.save(db)
        return app.to_dict()

    def withdraw_application(self, application_id: str) -> Dict[str, Any]:
        db = self.repo.load()
        aid = normalise_text(application_id)
        app = db["applications"].get(aid)
        if not app:
            raise NotFoundError("Application not found.")

        current = app["status"]
        if current in [ApplicationStatus.REJECTED.value, ApplicationStatus.WITHDRAWN.value]:
            raise StateError("Cannot withdraw a rejected/withdrawn application.")

        app["status"] = ApplicationStatus.WITHDRAWN.value
        app["updated_at"] = datetime.utcnow().isoformat()
        app["audit_trail"].append({"ts": datetime.utcnow().isoformat(), "action": "withdrawn", "details": {}})
        db["applications"][aid] = app
        self.repo.save(db)
        return app

    def get_application_status(self, application_id: str) -> Dict[str, Any]:
        db = self.repo.load()
        aid = normalise_text(application_id)
        app = db["applications"].get(aid)
        if not app:
            raise NotFoundError("Application not found.")
        return {
            "application_id": app["application_id"],
            "status": app["status"],
            "updated_at": app["updated_at"],
            "audit_trail": app.get("audit_trail", [])
        }

    def update_application_status(self, application_id: str, new_status: str, reason: str = "") -> Dict[str, Any]:
        db = self.repo.load()
        aid = normalise_text(application_id)
        app = db["applications"].get(aid)
        if not app:
            raise NotFoundError("Application not found.")

        ns = normalise_text(new_status)
        allowed = {
            ApplicationStatus.APPLIED.value: {ApplicationStatus.SCREENED.value, ApplicationStatus.REJECTED.value},
            ApplicationStatus.SCREENED.value: {ApplicationStatus.SHORTLISTED.value, ApplicationStatus.REJECTED.value},
            ApplicationStatus.SHORTLISTED.value: {ApplicationStatus.INTERVIEW_SCHEDULED.value, ApplicationStatus.REJECTED.value},
            ApplicationStatus.REJECTED.value: set(),
            ApplicationStatus.WITHDRAWN.value: set(),
            ApplicationStatus.INTERVIEW_SCHEDULED.value: set(),
        }

        cur = app["status"]
        if ns not in [s.value for s in ApplicationStatus]:
            raise ValidationError("Unknown status.")
        if ns == cur:
            raise ValidationError("Status unchanged.")
        if ns not in allowed.get(cur, set()):
            raise StateError(f"Invalid transition: {cur} -> {ns}")

        app["status"] = ns
        app["updated_at"] = datetime.utcnow().isoformat()
        app["audit_trail"].append(
            {"ts": datetime.utcnow().isoformat(), "action": "status_change", "details": {"from": cur, "to": ns, "reason": reason}}
        )
        db["applications"][aid] = app
        self.repo.save(db)
        return app

    def list_applications_for_job(self, job_id: str) -> List[Dict[str, Any]]:
        db = self.repo.load()
        jid = normalise_text(job_id)
        if jid not in db["jobs"]:
            raise NotFoundError("Job not found.")
        return [a for a in db["applications"].values() if a["job_id"] == jid]
