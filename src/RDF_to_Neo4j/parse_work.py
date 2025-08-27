from rdflib import Graph
from RDF_to_Neo4j.utils import get_id, get_ttl, get_title, get_contribution
from RDF_to_Neo4j.parse_instance import get_instance_infos
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
        if language_id == 'LangBo':
            language_ids.append('bo')
        else:
            language_ids.append(language_id)
    return {'languages': language_ids}


def parse_work_ttl(ttl_file, work_id):
    work_info = {}
    g = Graph()
    try:
        g.parse(data=ttl_file, format="ttl")
    except Exception as e:
        print("cant read ttl", work_id, e)
        return None
    title = get_title(g, work_id)
    language = get_language(g, work_id)
    contribution = get_contribution(g, work_id)
    # instance_infos = get_instance_infos(g, work_id)
    # work_info = {
    #     "expression_bdrc": work_id,
    #     "title": title,
    #     'language': language,
    #     "instance_infos": instance_infos,
    #     "contribution": contribution
    # }
    return work_info


def get_work_info(instance_id):
    ttl_file = get_ttl(instance_id)
    work_info = parse_work_ttl(ttl_file, instance_id)
    return work_info

