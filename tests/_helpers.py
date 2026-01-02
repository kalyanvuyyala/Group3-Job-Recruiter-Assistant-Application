import json
from pathlib import Path
from src.storage.repository import Repository

def make_repo(tmp_path):
    # isolated test database for each test run
    test_file = tmp_path / "test_db.json"
    test_file.write_text(json.dumps({"jobs": {}, "candidates": {}, "applications": {}, "interviews": {}}, indent=2))
    return Repository(filepath=test_file)
