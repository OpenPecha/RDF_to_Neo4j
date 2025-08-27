from RDF_to_Neo4j.parse_work import parse_work_ttl
from RDF_to_Neo4j.utils import get_ttl
import json
import hashlib

def write_json(data, file_name):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def pipeline(work_id):
    ttl_file = get_ttl(work_id)
    work_info = parse_work_ttl(ttl_file, work_id)
    write_json(work_info, f"data/{work_id}.json")

def get_hash(id):
    md5 = hashlib.md5(str.encode(id))
    two = md5.hexdigest()[:2]
    print(two)

if __name__ == "__main__":
    id = 'P6161'
    get_hash(id)
    pipeline("WA0RT3216")