import json
from pathlib import Path
from typing import Dict, Any
from src.app.config import DATA_FILE

DEFAULT_DB = {
    "jobs": {},
    "candidates": {},
    "applications": {},
    "interviews": {}
}

class Repository:
    def __init__(self, filepath: Path = DATA_FILE):
        self.filepath = filepath

    def load(self) -> Dict[str, Any]:
        if not self.filepath.exists():
            return dict(DEFAULT_DB)
        try:
            with self.filepath.open("r", encoding="utf-8") as f:
                data = json.load(f)
            for k in DEFAULT_DB.keys():
                data.setdefault(k, {})
            return data
        except (json.JSONDecodeError, OSError):
            return dict(DEFAULT_DB)

    def save(self, db: Dict[str, Any]) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, sort_keys=True)
