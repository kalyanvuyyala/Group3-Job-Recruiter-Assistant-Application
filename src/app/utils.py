import re
from typing import Any, Dict, List
from src.app.exceptions import ValidationError

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^\+?[0-9]{7,15}$")

def normalise_text(s: str) -> str:
    return " ".join((s or "").strip().split()).lower()

def validate_email(email: str) -> None:
    if not email or not _EMAIL_RE.match(email.strip()):
        raise ValidationError("Invalid email format.")

def validate_phone(phone: str) -> None:
    if not phone or not _PHONE_RE.match(phone.strip()):
        raise ValidationError("Invalid phone format.")

def validate_salary(min_salary: int, max_salary: int) -> None:
    if min_salary < 0 or max_salary < 0:
        raise ValidationError("Salary cannot be negative.")
    if min_salary > max_salary:
        raise ValidationError("Minimum salary cannot exceed maximum salary.")

def ensure_non_empty(field: str, value: str) -> None:
    if not value or not str(value).strip():
        raise ValidationError(f"{field} cannot be empty.")

def ensure_unique_id(existing: Dict[str, Any], obj_id: str, label: str) -> None:
    if obj_id in existing:
        raise ValidationError(f"{label} ID already exists: {obj_id}")

def normalise_skills(skills: List[str]) -> List[str]:
    clean = []
    for s in skills or []:
        t = normalise_text(s)
        if t and t not in clean:
            clean.append(t)
    return clean
