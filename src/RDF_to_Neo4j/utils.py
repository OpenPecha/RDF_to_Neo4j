import requests
from rdflib import Graph, Namespace
from rdflib.namespace import SKOS, Namespace
from pyewts import pyewts

converter = pyewts()

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")

def wylie_to_tibetan(wylie_text):
    """Convert Wylie transliteration to Tibetan Unicode"""
    try:
        result = converter.toUnicode(wylie_text)
        return result
    except Exception as e:
        print(f"Conversion error: {e}")


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

def get_creators(g, work_id):
    """
    Extract all creator information from RDF graph for a given work ID.
    
    Args:
        g: RDF graph object
        work_id: Work ID string
        
    Returns:
        list: List of creator dictionaries with person and role information
    """
    creators_info = []
    
    try:
        # Get all creator entities (AgentAsCreator) for this work
        creator_entities = list(g.objects(BDR[work_id], BDO["creator"]))
        
        for creator_entity in creator_entities:
            creator_data = {"contribution": {}}
            
            # Get the person (agent) information
            try:
                agents = list(g.objects(creator_entity, BDO["agent"]))
                if agents:
                    person_uri = agents[0]
                    person_id = get_id(str(person_uri))
                    
                    # Get person's name using the title parsing function
                    person_name_info = get_title(g, person_id)
                    
                    creator_data["contribution"]["person"] = {
                        "name": person_name_info,
                        "bdrc": person_id
                    }
            except Exception as e:
                print(f"Error getting agent for creator {creator_entity}: {e}")
                creator_data["contribution"]["person"] = {
                    "name": None,
                    "bdrc": None
                }
            
            # Get the role information
            try:
                roles = list(g.objects(creator_entity, BDO["role"]))
                if roles:
                    role_uri = roles[0]
                    role_id = get_id(str(role_uri))
                    creator_data["contribution"]["role"] = role_id
                else:
                    creator_data["contribution"]["role"] = None
            except Exception as e:
                print(f"Error getting role for creator {creator_entity}: {e}")
                creator_data["contribution"]["role"] = None
            
            # Get creation event type if it exists
            try:
                event_types = list(g.objects(creator_entity, BDO["creationEventType"]))
                if event_types:
                    event_type_uri = event_types[0]
                    event_type_id = get_id(str(event_type_uri))
                    creator_data["contribution"]["creationEventType"] = event_type_id
            except Exception as e:
                # This is optional, so don't print error
                pass
            
            creators_info.append(creator_data)
            
    except Exception as e:
        print(f"Error getting creators for work {work_id}: {e}")
    
    return creators_info


def get_contribution(g, id):
    creators = get_creators(g, id)
    return creators


def get_title(g, id):
    """
    Extract title information from RDF graph for a given entity ID.
    
    Args:
        g: RDF graph object
        id: Entity ID string
        
    Returns:
        dict: Dictionary containing 'main_title', 'alternative_titles', and 'has_titles'
              Each title is a dict with 'text' and 'code' keys
    """
    def process_title_literal(literal):
        text = str(literal) 
        lang_code = literal.language if hasattr(literal, 'language') else None

        if lang_code == 'bo-x-ewts':
            converted_text = wylie_to_tibetan(text)
            return {'text': converted_text, 'code': 'bo'}
        else:
            return {'text': text, 'code': lang_code}
    
    title_info = {
        'main': None,
        'alternative': [],
        'has_titles': []
    }
    
    # Get prefLabel as main title
    try:
        pref_labels = list(g.objects(BDR[id], SKOS.prefLabel))
        if pref_labels:
            title_info['main'] = process_title_literal(pref_labels[0])
    except Exception as e:
        print(f"Error getting prefLabel for {id}: {e}")
    
    # Get all altLabels as alternative titles
    try:
        alt_labels = list(g.objects(BDR[id], SKOS.altLabel))
        for alt_label in alt_labels:
            processed_title = process_title_literal(alt_label)
            title_info['alternative'].append(processed_title)
    except Exception as e:
        print(f"Error getting altLabels for {id}: {e}")
    
    # Check for hasTitle property (bdo:hasTitle)
    try:
        has_titles = list(g.objects(BDR[id], BDO["hasTitle"]))
        for has_title in has_titles:
            processed_title = process_title_literal(has_title)
            title_info['has_titles'].append(processed_title)
    except Exception as e:
        print(f"Error getting hasTitle for {id}: {e}")
    
    return {'titles': title_info}