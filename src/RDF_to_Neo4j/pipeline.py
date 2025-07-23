from RDF_to_Neo4j.parse_instance import parse_instance_ttl, get_instance_list
from RDF_to_Neo4j.parse_work import parse_work_ttl
import json


def write_instance_info(instance_info, instance_id):
    with open(f"instance_info/{instance_id}.json", "w") as f:
        json.dump(instance_info, f)

def pipeline(work_id):
    instance_ids = get_instance_list(work_id)
    for instance_id in instance_ids:
        instance_info = parse_instance_ttl(instance_id, work_id)
        write_instance_info(instance_info, instance_id)
    

if __name__ == "__main__":
    pipeline("WA0RK0529")