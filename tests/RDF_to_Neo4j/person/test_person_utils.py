from unittest.mock import patch
from RDF_to_Neo4j.person.person_utils import PersonUtils
from RDF_to_Neo4j.constant import get_constant
from rdflib import Graph
import rdflib

MOCK_WORK_ID = "WA0RK0013"
MOCK_ROLE_ID = "R0ER0026"

def get_graph_for_test(mock_ttl_file, mock_work_id):
    g = Graph()
    try:
        return g.parse(data=mock_ttl_file, format=get_constant("FORMAT_TTL"))
    except ValueError as e:
        raise ValueError(f"cant read ttl {mock_work_id} {e}")
    
def test_get_contribution():
    mock_work_id = MOCK_WORK_ID
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)

    expected_contribution = [{'person_bdrc_id': 'P8182', 'role': {'text': 'translator', 'code': 'en'}}]

    response = PersonUtils.get_contribution(g, mock_work_id)
    
    assert response == expected_contribution

def test_get_role():
    mock_work_id = MOCK_WORK_ID
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)

    mock_creator_entity = rdflib.term.URIRef('http://purl.bdrc.io/resource/CRWA0RK0013_ATII0')

    mock_role_id = "R0ER0026"

    mock_role = {'text': 'translator', 'code': 'en'}

    with patch("RDF_to_Neo4j.person.person_utils.PersonUtils.get_id", return_value=mock_role_id), \
        patch("RDF_to_Neo4j.person.person_utils.PersonUtils.get_person_role", return_value=mock_role):

        response = PersonUtils.get_role(g, mock_creator_entity)

        assert response == mock_role

def test_get_person_id():
    mock_work_id = MOCK_WORK_ID
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)

    mock_creator_entity = rdflib.term.URIRef('http://purl.bdrc.io/resource/CRWA0RK0013_ATII0')

    mock_person_id = "P8182"

    with patch("RDF_to_Neo4j.person.person_utils.PersonUtils.get_id", return_value=mock_person_id):

        response = PersonUtils.get_person_id(g, mock_creator_entity)

        assert response == mock_person_id

def test_get_person_role():
    mock_role_id = MOCK_ROLE_ID
    with open("tests/RDF_to_Neo4j/mock_R0ER0026_person_role.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    expected_role = {'text': 'translator', 'code': 'en'}

    with patch("RDF_to_Neo4j.person.person_utils.TTLUtils.get_ttl", return_value=mock_ttl_file):

        response = PersonUtils.get_person_role(mock_role_id)

        assert response == expected_role
    