from rdflib import Graph
from RDF_to_Neo4j.utils import get_id, get_ttl, get_label
from RDF_to_Neo4j.parse_instance import parse_instance_ttl, get_instance_ids
from rdflib.namespace import Namespace


BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")



def is_root(g, work_id):
    is_root = bool(list(g.objects(BDR[work_id], BDO["isRoot"]))[0].split(",")[0])
    return is_root


def get_language(g, work_id):
    language_ids = []
    languages = g.objects(BDR[work_id], BDO["language"])
    for language in languages:
        language_id = get_id(str(language))
        language_ids.append(language_id)
    return language_ids



def get_instance_info(g, work_id):
    instance_list = []
    instance_ids = get_instance_ids(g, work_id)
    for instance_id in instance_ids:
        instance_info = parse_instance_ttl(instance_id, work_id)
        instance_list.append(instance_info)
    return instance_list
    

def parse_work_ttl(ttl_file, work_id):
    work_info = {}
    g = Graph()
    try:
        g.parse(data=ttl_file, format="ttl")
    except Exception as e:
        print("cant read ttl", work_id, e)
        return None
    title = get_label(g, work_id)
    instance_info = get_instance_info(g, work_id)
    work_info = {
        "work_id": work_id,
        "title": title,
        "instance_info": instance_info
    }
    return work_info


def get_work_info(instance_id):
    ttl_file = get_ttl(instance_id)
    work_info = parse_work_ttl(ttl_file, instance_id)
    return work_info

