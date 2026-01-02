from typing import Dict, Any
from datetime import datetime, timedelta
from src.app.exceptions import ValidationError, NotFoundError, ConflictError
from src.app.utils import normalise_text, ensure_non_empty
from src.domain.models import Interview
from src.domain.enums import ApplicationStatus
from src.storage.repository import Repository

class InterviewService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def schedule_interview(self, interview_id: str, application_id: str, scheduled_time_iso: str,
                           duration_minutes: int, interviewer: str, location: str = "online") -> Dict[str, Any]:
        db = self.repo.load()
        ensure_non_empty("interview_id", interview_id)
        ensure_non_empty("application_id", application_id)
        ensure_non_empty("interviewer", interviewer)

        iid = normalise_text(interview_id)
        aid = normalise_text(application_id)
        if iid in db["interviews"]:
            raise ValidationError("Interview ID already exists.")

        app = db["applications"].get(aid)
        if not app:
            raise NotFoundError("Application not found.")

        if app["status"] != ApplicationStatus.SHORTLISTED.value:
            raise ValidationError("Interview can only be scheduled for SHORTLISTED applications.")

        try:
            start = datetime.fromisoformat(scheduled_time_iso)
        except ValueError:
            raise ValidationError("scheduled_time must be ISO format.")

        if duration_minutes <= 0 or duration_minutes > 240:
            raise ValidationError("duration_minutes must be between 1 and 240.")

        end = start + timedelta(minutes=int(duration_minutes))
        interviewer_norm = " ".join(interviewer.strip().split()).lower()

        for itv in db["interviews"].values():
            if itv.get("cancelled"):
                continue
            if itv["interviewer"].lower() != interviewer_norm:
                continue
            existing_start = datetime.fromisoformat(itv["scheduled_time"])
            existing_end = existing_start + timedelta(minutes=int(itv["duration_minutes"]))
            overlap = (start < existing_end) and (end > existing_start)
            if overlap:
                raise ConflictError("Interviewer is double-booked.")

        interview = Interview(
            interview_id=iid,
            application_id=aid,
            scheduled_time=start.isoformat(),
            duration_minutes=int(duration_minutes),
            interviewer=interviewer_norm,
            location=" ".join(location.strip().split()) if location else "online",
            cancelled=False
        )
        db["interviews"][iid] = interview.to_dict()

        app["status"] = ApplicationStatus.INTERVIEW_SCHEDULED.value
        app["audit_trail"].append({"ts": datetime.utcnow().isoformat(), "action": "interview_scheduled", "details": {"interview_id": iid}})
        app["updated_at"] = datetime.utcnow().isoformat()
        db["applications"][aid] = app

        self.repo.save(db)
        return interview.to_dict()
