import json
from pathlib import Path


def check_for_empties(data, path=""):
    empties = []
    if isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, list) and len(item) == 0:
                empties.append({"type": "empty_list", "path": f"{path}[{i}]"})
            elif isinstance(item, dict) and len(item) == 0:
                empties.append({"type": "empty_dict", "path": f"{path}[{i}]"})
            else:
                empties.extend(check_for_empties(item, f"{path}[{i}]"))
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 0:
                empties.append({"type": "empty_list", "path": f"{path}.{key}" if path else key})
            elif isinstance(value, dict) and len(value) == 0:
                empties.append({"type": "empty_dict", "path": f"{path}.{key}" if path else key})
            else:
                empties.extend(check_for_empties(value, f"{path}.{key}" if path else key))
    return empties


def check_person_data():
    results = []
    data_path = Path("data")
    for json_file in data_path.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        if isinstance(file_data, list):
            for person_idx, person in enumerate(file_data):
                person_empties = check_for_empties(person, f"person[{person_idx}]")
                for empty in person_empties:
                    results.append({
                        "file": json_file.name,
                        "bdrc_id": person.get("bdrc_id", "unknown"),
                        "empty_type": empty["type"],
                        "path": empty["path"],
                        "person_data": person
                    })
    return results


def main():
    results = check_person_data()
    with open("empty_data_cases.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
