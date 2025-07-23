from rdflib import Graph, Namespace
from utils import get_id, get_ttl, get_title


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


def get_creator(g, instance_id):
    creator = get_id(str(list(g.objects(BDR[instance_id], BDO["instanceOfWork"]))[0]))
    return creator


def get_contribution(g, instance_id):
    contribution = get_id(str(list(g.objects(BDR[instance_id], BDO["instanceOfWork"]))[0]))
    return contribution


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
        "manifestation_of": work_id,
        "has_contribution": contribution,
        "Title": title
    }
    return instance_info

def get_instance_list(work_id):
    ttl_file = get_ttl(work_id)
    g = Graph()
    g.parse(data=ttl_file, format="ttl")
    instance_ids = get_instance_ids(g, work_id)
    return instance_ids
