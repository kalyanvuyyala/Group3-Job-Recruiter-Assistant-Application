import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

from src.app.exceptions import ValidationError
from src.app.utils import normalise_text
from src.storage.repository import Repository


class BulkImportService:
    """
    Bulk import into the JSON data store.
    Expected JSON format:
    {
      "jobs": [ {...}, {...} ],
      "candidates": [ {...}, {...} ],
      "applications": [ {...}, {...} ],
      "interviews": [ {...}, {...} ]
    }
    """

    def __init__(self, repo: Repository):
        self.repo = repo

    def import_from_json(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise ValidationError("Bulk file not found.")

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON file.")

        if not isinstance(payload, dict):
            raise ValidationError("Bulk JSON must be an object.")

        db = self.repo.load()

        report = {
            "jobs": {"imported": 0, "skipped": 0, "errors": []},
            "candidates": {"imported": 0, "skipped": 0, "errors": []},
            "applications": {"imported": 0, "skipped": 0, "errors": []},
            "interviews": {"imported": 0, "skipped": 0, "errors": []},
        }

        self._merge_section(db, payload, "jobs", "job_id", report)
        self._merge_section(db, payload, "candidates", "candidate_id", report)
        self._merge_section(db, payload, "applications", "application_id", report)
        self._merge_section(db, payload, "interviews", "interview_id", report)

        self.repo.save(db)
        return report

    def _merge_section(
        self,
        db: Dict[str, Any],
        payload: Dict[str, Any],
        section: str,
        id_field: str,
        report: Dict[str, Any]
    ) -> None:
        items = payload.get(section, [])
        if items is None:
            return
        if not isinstance(items, list):
            raise ValidationError(f'"{section}" must be a list.')

        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                report[section]["skipped"] += 1
                report[section]["errors"].append(f"{section}[{idx}]: not an object")
                continue

            raw_id = item.get(id_field)
            if not raw_id or not str(raw_id).strip():
                report[section]["skipped"] += 1
                report[section]["errors"].append(f"{section}[{idx}]: missing {id_field}")
                continue

            obj_id = normalise_text(str(raw_id))
            if obj_id in db[section]:
                report[section]["skipped"] += 1
                continue

            # Store with normalised ID
            item[id_field] = obj_id
            db[section][obj_id] = item
            report[section]["imported"] += 1
