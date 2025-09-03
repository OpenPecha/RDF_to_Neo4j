from constant import get_constant
from rdflib import Graph
from rdflib.namespace import SKOS
from utils import Utils
from ttl_utils import TTLUtils

BDR = get_constant("BDR")
BDO = get_constant("BDO")

class PersonUtils:

    @staticmethod
    def get_id(uri: str):
        if uri == "None":
            return None
        return uri.split("/")[-1]
    
    @staticmethod
    def find_english_label(labels):
        for label in labels:
            if hasattr(label, 'language') and label.language == 'en':
                return Utils.process_title_literal(label)
        return None
    
    @staticmethod
    def find_tibetan_label(labels):
        for label in labels:
            if hasattr(label, 'language') and label.language in ['bo', 'bo-x-ewts']:
                return Utils.process_title_literal(label)
        return None

    @staticmethod
    def get_person_role(role_id):
        """
        Extract role information with language preference: English first, then Tibetan.
        
        Args:
            role_id: Role ID string
            
        Returns:
            dict: Role information with 'text' and 'code' keys, or None if not found
        """
        role_ttl = TTLUtils.get_ttl(role_id)
        if not role_ttl:
            return None
            
        g = Graph()
        g.parse(data=role_ttl, format="ttl")
        
        pref_labels = list(g.objects(BDR[role_id], SKOS.prefLabel))
        if pref_labels:
            english_pref = PersonUtils.find_english_label(pref_labels)
            if english_pref:
                return english_pref
        
        alt_labels = list(g.objects(BDR[role_id], SKOS.altLabel))
        if alt_labels:
            english_alt = PersonUtils.find_english_label(alt_labels)
            if english_alt:
                return english_alt
        
        if pref_labels:
            tibetan_pref = PersonUtils.find_tibetan_label(pref_labels)
            if tibetan_pref:
                return tibetan_pref
        
        if alt_labels:
            tibetan_alt = PersonUtils.find_tibetan_label(alt_labels)
            if tibetan_alt:
                return tibetan_alt
        
        if pref_labels:
            return Utils.process_title_literal(pref_labels[0])
        elif alt_labels:
            return Utils.process_title_literal(alt_labels[0])
        
        return None
    
    @staticmethod
    def get_person_id(g, creator_entity):
        person_id = None
        try:
            agents = list(g.objects(creator_entity, BDO["agent"]))
            if agents:
                person_uri = agents[0]
                person_id = PersonUtils.get_id(str(person_uri))
        except Exception as e:
            print(f"Error getting agent for creator {creator_entity}: {e}")

        return person_id
    
    @staticmethod
    def get_role(g, creator_entity):
        role = None
        try:
            roles = list(g.objects(creator_entity, BDO["role"]))
            if roles:
                role_uri = roles[0]
                role_id = PersonUtils.get_id(str(role_uri))
                role = PersonUtils.get_person_role(role_id)
        except Exception as e:
            print(f"Error getting role for creator {creator_entity}: {e}")
        return role


    @staticmethod
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
                person_id = PersonUtils.get_person_id(g, creator_entity)
                if not person_id:
                    continue

                if person_id in seen_bdrc_ids:
                    continue

                seen_bdrc_ids.add(person_id)
                    
                contribution = {
                    "person_bdrc_id": person_id,
                    "role": None
                }

                person_role = PersonUtils.get_role(g, creator_entity)

                if person_role:
                    contribution["role"] = person_role
                
                contributions.append(contribution)
                
        except Exception as e:
            print(f"Error getting creators for work {work_id}: {e}")
        return contributions