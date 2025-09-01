from pathlib import Path
import json
import csv
import requests

def process_name(names):
    if isinstance(names, list):
        # Merge list of dicts into single dict
        merged_name = {}
        for item in names:
            merged_name.update(item)
        return merged_name
    else:
        return names


def upload_person_data():
    # Load uploaded IDs from CSV
    uploaded_ids = set()
    csv_file = "uploaded_persons.csv"
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row:
                    uploaded_ids.add(row[0])
    except FileNotFoundError:
        pass

    # Process JSON files
    for json_file in Path("data").glob("*.json"):
        with open(json_file, "r") as f:
            persons = json.load(f)
        print(json_file.name)
        for person in persons:
            person_id = person["bdrc_id"]
            # Skip if already uploaded
            # if person_id in uploaded_ids:
            #     continue
            if person_id != "P2KG209992":
                continue
                
            alt_names = []
            for alt_name in person["alt_names"]:
                alt_names.append(process_name(alt_name))
            
            # Upload to API
            response = requests.post("https://api-l25bgmwqoa-uc.a.run.app/v2/persons", json=data)
            
            if response.status_code in [200, 201]:
                # Add to CSV
                with open(csv_file, 'a', newline='') as f:
                    if f.tell() == 0:  # File is empty, add header
                        csv.writer(f).writerow(['person_id'])
                    csv.writer(f).writerow([person_id])
                uploaded_ids.add(person_id)
                print(f"Uploaded {person_id}")

if __name__ == "__main__":
    upload_person_data()   