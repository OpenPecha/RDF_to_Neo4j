import requests
from rdflib import Graph, Namespace
from rdflib.namespace import SKOS, OWL, Namespace, NamespaceManager, XSD

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")

def get_ttl(id):
    try:
        ttl = requests.get(f"https://ldspdi.bdrc.io/resource/{id}.ttl")
        return ttl.text
    except Exception as e:
        print(" TTL not Found!!!", e)
        return None

def get_id(URI):
    if URI == "None":
        return None
    return URI.split("/")[-1]


def get_title(g, id):
    prefLabel = str(list(g.objects(BDR[id], SKOS.prefLabel))[0])
    altLabel = str(list(g.objects(BDR[id], SKOS.altLabel))[0])
    return prefLabel