from RDF_to_Neo4j.parse_work import parse_work_ttl
from RDF_to_Neo4j.utils import get_ttl
import json


def write_json(data, file_name):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def pipeline(work_id):
    ttl_file = get_ttl(work_id)
    work_info = parse_work_ttl(ttl_file, work_id)
    write_json(work_info, f"data/{work_id}.json")   
        

if __name__ == "__main__":
    pipeline("WA0RK0529")