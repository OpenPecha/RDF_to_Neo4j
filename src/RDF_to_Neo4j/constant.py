from rdflib import Namespace

CONSTANT = {
    "BDR": Namespace("http://purl.bdrc.io/resource/"),
    "BDO": Namespace("http://purl.bdrc.io/ontology/core/"),
    
    "TTL_URL": "https://ldspdi.bdrc.io/resource",

    "FORMAT_TTL": "ttl"
}

def get_constant(key: str):
    if key not in CONSTANT:
        raise ValueError(f"Invalid key: {key}")
    return CONSTANT[key]