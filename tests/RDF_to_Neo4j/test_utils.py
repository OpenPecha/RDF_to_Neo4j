from unittest.mock import patch, Mock
from RDF_to_Neo4j.utils import Utils
import rdflib


def test_wylie_to_tibetan():
    
    mock_wylie_text = "rdo rje gcod pa/"
    mock_converted_wylie_text_to_tibetan = "རྡོ་རྗེ་གཅོད་པ།"

    with patch("RDF_to_Neo4j.utils.converter.toUnicode", return_value=mock_converted_wylie_text_to_tibetan):

        tibetan_text = Utils.wylie_to_tibetan(mock_wylie_text)

        assert tibetan_text == mock_converted_wylie_text_to_tibetan

def test_process_title_literal():

    response = Utils.process_title_literal(rdflib.term.Literal('phags pa shes rab kyi pha rol tu phyin pa rdo rje gcod pa/', lang='bo-x-ewts'))

    assert response == {'text': 'ཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ།', 'code': 'bo'}