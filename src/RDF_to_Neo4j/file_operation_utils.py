import json
from pathlib import Path

class FileOperationUtils:

    @staticmethod
    def write_json(data, file_name):
        base_dir = Path(__file__).resolve().parent / "output"
        base_dir.mkdir(parents=True, exist_ok=True)
        file_path = base_dir / f"{file_name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)