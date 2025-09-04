from pyewts import pyewts
from constant import get_constant
import hashlib

converter = pyewts()

BDR = get_constant("BDR")
BDO = get_constant("BDO")

class Utils:

    @staticmethod
    def wylie_to_tibetan(wylie_text):
        """Convert Wylie transliteration to Tibetan Unicode"""
        try:
            result = converter.toUnicode(wylie_text)
            return result
        except Exception as e:
            print(f"Conversion error: {e}")

    @staticmethod
    def process_title_literal(literal):
        text = str(literal) 
        lang_code = literal.language if hasattr(literal, 'language') else None

        if lang_code == 'bo-x-ewts':
            converted_text = Utils.wylie_to_tibetan(text)
            return {'text': converted_text, 'code': 'bo'}
        else:
            return {'text': text, 'code': lang_code}
        
    @staticmethod
    def get_hash(id):
        md5 = hashlib.md5(str.encode(id))
        two = md5.hexdigest()[:2]
        print(two)

'''
def get_role(role_id):
    """
    Extract role information with language preference: English first, then Tibetan.
    
    Args:
        role_id: Role ID string
        
    Returns:
        dict: Role information with 'text' and 'code' keys, or None if not found
    """
    role_ttl = get_ttl(role_id)
    if not role_ttl:
        return None
        
    g = Graph()
    g.parse(data=role_ttl, format="ttl")
    
    def find_english_label(labels):
        for label in labels:
            if hasattr(label, 'language') and label.language == 'en':
                return Utils.process_title_literal(label)
        return None
    
    def find_tibetan_label(labels):
        for label in labels:
            if hasattr(label, 'language') and label.language in ['bo', 'bo-x-ewts']:
                return Utils.process_title_literal(label)
        return None
    
    pref_labels = list(g.objects(BDR[role_id], SKOS.prefLabel))
    if pref_labels:
        english_pref = find_english_label(pref_labels)
        if english_pref:
            return english_pref
    
    alt_labels = list(g.objects(BDR[role_id], SKOS.altLabel))
    if alt_labels:
        english_alt = find_english_label(alt_labels)
        if english_alt:
            return english_alt
    
    if pref_labels:
        tibetan_pref = find_tibetan_label(pref_labels)
        if tibetan_pref:
            return tibetan_pref
    
    if alt_labels:
        tibetan_alt = find_tibetan_label(alt_labels)
        if tibetan_alt:
            return tibetan_alt
    
    if pref_labels:
        return Utils.process_title_literal(pref_labels[0])
    elif alt_labels:
        return Utils.process_title_literal(alt_labels[0])
    
    return None


def get_person_name(person_id):
    """
    Extract person name information from RDF graph for a given person ID.
    
    Args:
        person_id: Person ID string
        
    Returns:
        dict: Dictionary containing person name information with 'main', 'alternative', and 'has_titles'
    """
    person_ttl = TTLUtils.get_ttl(person_id)
    if not person_ttl:
        return {'names': {'main': None, 'alternative': [], 'has_titles': []}}
    
    g = Graph()
    g.parse(data=person_ttl, format="ttl")
    
    name_info = {
        'main': None,
        'alternative': []
    }
    
    try:
        pref_labels = list(g.objects(BDR[person_id], SKOS.prefLabel))
        if pref_labels:
            name_info['main'] = Utils.process_title_literal(pref_labels[0])
    except Exception as e:
        print(f"Error getting prefLabel for person {person_id}: {e}")
    
    try:
        person_names = list(g.objects(BDR[person_id], BDO["personName"]))
        for person_name_entity in person_names:
            labels = list(g.objects(person_name_entity, RDFS.label))
            for label in labels:
                processed_name = Utils.process_title_literal(label)
                if name_info['main'] and processed_name['text'] != name_info['main']['text']:
                    name_info['alternative'].append(processed_name)
                elif not name_info['main']:
                    name_info['alternative'].append(processed_name)
    except Exception as e:
        print(f"Error getting personName for {person_id}: {e}")
    
    return {'names': name_info}


def get_contribution(g, work_id):
    """
    Extract all creator information from RDF graph for a given work ID.
    Avoids duplicate persons by checking BDRC IDs.
    
    Args:
        g: RDF graph object
        work_id: Work ID string
         
    Returns:
        list: List of unique contribution dictionaries with person and role information
    """
    contributions = []
    seen_bdrc_ids = set()
    
    try:
        creator_entities = list(g.objects(BDR[work_id], BDO["creator"]))
        
        for creator_entity in creator_entities:
            person_id = None
            
            try:
                agents = list(g.objects(creator_entity, BDO["agent"]))
                if agents:
                    person_uri = agents[0]
                    person_id = get_id(str(person_uri))
                    if person_id in seen_bdrc_ids:
                        continue
                    
                    seen_bdrc_ids.add(person_id)
                    
            except Exception as e:
                print(f"Error getting agent for creator {creator_entity}: {e}")
                continue

            if not person_id:
                continue
                
            contribution = {
                "person": {
                    "bdrc": person_id,
                    "name": {
                        "main": None,
                        "alternative": []
                    }
                },
                "role": None
            }
            
            try:
                person_name_data = get_person_name(person_id)
                if person_name_data and 'names' in person_name_data:
                    contribution["person"]["name"] = person_name_data['names']
            except Exception as e:
                print(f"Error getting person name for {person_id}: {e}")
            
            try:
                roles = list(g.objects(creator_entity, BDO["role"]))
                if roles:
                    role_uri = roles[0]
                    role_id = get_id(str(role_uri))
                    role = get_role(role_id)
                    contribution["role"] = role
                    
            except Exception as e:
                print(f"Error getting role for creator {creator_entity}: {e}")
            
            contributions.append(contribution)
            
    except Exception as e:
        print(f"Error getting creators for work {work_id}: {e}")
    
    return contributions

'''