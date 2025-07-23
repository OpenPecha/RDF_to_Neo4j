from rdflib import Graph, Namespace
from RDF_to_Neo4j.utils import get_id, get_ttl, get_title, get_contribution


BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")


def get_instance_ids(g, work_id):
    scan_ids = []
    instance_ids = []
    instances = list(g.objects(BDR[work_id], BDO["workHasInstance"]))
    for instance in instances:
        id = get_id(str(instance))
        instance_ids.append(id)
    return instance_ids 


def get_work_id(g, instance_id):
    work_id = get_id(str(list(g.objects(BDR[instance_id], BDO["instanceOfWork"]))[0]))
    return work_id



def parse_instance_ttl(instance_id):
    instance_info = {}
    ttl_file = get_ttl(instance_id)
    g = Graph()
    try:
        g.parse(data=ttl_file, format="ttl")
    except Exception as e:
        print("cant read ttl", instance_id, e)
        return None
    title = get_title(g, instance_id)
    work_id = get_work_id(g, instance_id)
    contribution = get_contribution(g, instance_id)
    instance_info = {
        "manifestation_bdrc": instance_id,
        "has_contribution": contribution,
        "title": title
    }
    return instance_info

def get_instance_infos(instance_ids):
    instance_infos = []
    for instance_id in instance_ids:
        instance_info = parse_instance_ttl(instance_id)
        instance_infos.append(instance_info)
    return instance_infos