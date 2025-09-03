from rdflib import Graph
from rdflib.namespace import SKOS
from constant import get_constant
from utils import Utils
from ttl_utils import TTLUtils
from person.person_utils import PersonUtils

from typing import Dict, Any


BDR = get_constant("BDR")
BDO = get_constant("BDO")


class ParseWork:

    @staticmethod
    def parse_work_ttl(ttl_file, work_id) -> Dict[str, Any]:
        work_info = {}
        g = Graph()
        try:
            g.parse(data=ttl_file, format=get_constant("FORMAT_TTL"))
        except ValueError as e:
            raise ValueError(f"cant read ttl {work_id} {e}")
        title = ParseWork.get_title(g, work_id)
        language = ParseWork.get_language(g, work_id)
        contribution = PersonUtils.get_contribution(g, work_id)
        work_info = {
            "expression_bdrc": work_id,
            "title": title,
            'language': language,
            "contribution": contribution
        }
        return work_info
    
    @staticmethod
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
        title_info = {
            'main': None,
            'alternative': [],
            'has_titles': []
        }
        
        title_info['main'] = ParseWork.get_pref_lable(g, id)
        title_info['alternative'] = ParseWork.get_alt_lable(g, id)
        title_info['has_titles'] = ParseWork.get_has_titles(g, id)

        return {
            'titles': title_info
        }
    
    @staticmethod
    def get_pref_lable(g, id):
        try:
            pref_labels = list(g.objects(BDR[id], SKOS.prefLabel))
            if pref_labels:
                return Utils.process_title_literal(pref_labels[0])
        except Exception as e:
            print(f"Error getting prefLabel for {id}: {e}")

    @staticmethod
    def get_alt_lable(g, id):
        alt_lable = []
        try:
            alt_labels = list(g.objects(BDR[id], SKOS.altLabel))
            for alt_label in alt_labels:
                processed_title = Utils.process_title_literal(alt_label)
                alt_lable.append(processed_title)
        except Exception as e:
            print(f"Error getting altLabels for {id}: {e}")
        return alt_lable
    
    @staticmethod
    def get_has_titles(g, id):
        has_titles = []
        try:
            has_titles = list(g.objects(BDR[id], BDO["hasTitle"]))
            for has_title in has_titles:
                title_id = PersonUtils.get_id(str(has_title))
                processed_title = ParseWork.get_title_from_id(title_id)
                has_titles.append(processed_title)
        except Exception as e:
            print(f"Error getting hasTitle for {id}: {e}")
        return has_titles
        
        
    @staticmethod
    def get_title_from_id(id):
        ttl = TTLUtils.get_ttl(id)
        if not ttl:
            return None
        g = Graph()
        g.parse(data=ttl, format="ttl")
        title_info = {
            'main': None,
            'alternative': []
        }
        try:
            pref_labels = list(g.objects(BDR[id], SKOS.prefLabel))
            if pref_labels:
                title_info['main'] = Utils.process_title_literal(pref_labels[0])
        except Exception as e:
            print(f"Error getting prefLabel for {id}: {e}")
        
        try:
            alt_labels = list(g.objects(BDR[id], SKOS.altLabel))
            for alt_label in alt_labels:
                processed_title = Utils.process_title_literal(alt_label)
                title_info['alternative'].append(processed_title)
        except Exception as e:
            print(f"Error getting altLabels for {id}: {e}")
        return title_info
    
    @staticmethod
    def is_root(g, work_id):
        is_root = bool(list(g.objects(BDR[work_id], BDO["isRoot"]))[0].split(",")[0])
        return is_root

    @staticmethod
    def get_language(g, work_id):
        language_ids = []
        languages = g.objects(BDR[work_id], BDO["language"])
        for language in languages:
            language_id = PersonUtils.get_id(str(language))
            if language_id == 'LangBo':
                language_ids.append('bo')
            else:
                language_ids.append(language_id)
        return {'languages': language_ids}

    @staticmethod
    def get_work_info(instance_id):
        ttl_file = TTLUtils.get_ttl(instance_id)
        work_info = ParseWork.parse_work_ttl(ttl_file, instance_id)
        return work_info

