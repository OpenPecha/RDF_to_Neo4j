from unittest.mock import patch, Mock
from RDF_to_Neo4j.work.parse_work import ParseWork
from rdflib import Graph
from RDF_to_Neo4j.constant import get_constant

MOCK_WORK_ID = "WA0RK0013"

def get_graph_for_test(mock_ttl_file, mock_work_id):
    g = Graph()
    try:
        return g.parse(data=mock_ttl_file, format=get_constant("FORMAT_TTL"))
    except ValueError as e:
        raise ValueError(f"cant read ttl {mock_work_id} {e}")
     

def test_parse_work_ttl():

    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    mock_work_id = MOCK_WORK_ID 

    mock_work_ttl_title = {'titles': {'main': {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, 'alternative': [{'text': 'འཕགས་པ་མདོ་སྡུད་པ།', 'code': 'bo'}, {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཡན་ཏ་རིན་པོ་ཆེ་སྡུད་པ།', 'code': 'bo'}, {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཡོན་ཏན་རིན་པོ་ཆེ་སྡུད་པ།', 'code': 'bo'}, {'text': 'བཅོམ་ལྡན་འདས་མ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, {'text': 'མདོ་སྡུད་པ།', 'code': 'bo'}, {'text': 'སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, {'text': 'ᠬᠣᠳᠣᠬ ᠳᠣ ᠪᠢᠯᠢᠺ\u202fᠦᠨ ᠴᠢᠨᠠᠳᠣ ᠭᠢᠵᠠᠭᠠᠷ\u180eᠠ ᠭᠥᠷᠥᠭᠰᠡᠨ ᠬᠣᠷᠢᠶᠠᠩᠭᠣᠢ ᠰᠢᠯᠥᠭ', 'code': 'cmg-Mong'}, {'text': 'qutug tu bilig ün cinadu kijagar a kürügsen quriyanggui silüg', 'code': 'cmg-x-poppe'}], 'has_titles': []}}

    mock_work_ttl_language = {'languages': ['bo']}

    mock_work_ttl_contribution = [{'person_bdrc_id': 'P8182', 'role': {'text': 'translator', 'code': 'en'}}]

    expected_work_info = {
        "expression_bdrc": "WA0RK0013",
        "title": mock_work_ttl_title,
        "language": mock_work_ttl_language,
        "contribution": mock_work_ttl_contribution
    }

    with patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_title", return_value=mock_work_ttl_title), \
        patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_language", return_value=mock_work_ttl_language), \
        patch("RDF_to_Neo4j.work.parse_work.PersonUtils.get_contribution", return_value=mock_work_ttl_contribution):
        
        response = ParseWork.parse_work_ttl(mock_ttl_file, mock_work_id)
        
        assert response == expected_work_info

def test_get_title():

    mock_work_id = MOCK_WORK_ID

    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)

    mock_title_info_main = {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}
    mock_title_info_alternative = [{'text': 'འཕགས་པ་མདོ་སྡུད་པ།', 'code': 'bo'}, {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཡན་ཏ་རིན་པོ་ཆེ་སྡུད་པ།', 'code': 'bo'}, {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཡོན་ཏན་རིན་པོ་ཆེ་སྡུད་པ།', 'code': 'bo'}, {'text': 'བཅོམ་ལྡན་འདས་མ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, {'text': 'མདོ་སྡུད་པ།', 'code': 'bo'}, {'text': 'སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, {'text': 'ᠬᠣᠳᠣᠬ ᠳᠣ ᠪᠢᠯᠢᠺ\u202fᠦᠨ ᠴᠢᠨᠠᠳᠣ ᠭᠢᠵᠠᠭᠠᠷ\u180eᠠ ᠭᠥᠷᠥᠭᠰᠡᠨ ᠬᠣᠷᠢᠶᠠᠩᠭᠣᠢ ᠰᠢᠯᠥᠭ', 'code': 'cmg-Mong'}, {'text': 'qutug tu bilig ün cinadu kijagar a kürügsen quriyanggui silüg', 'code': 'cmg-x-poppe'}]
    mock_title_info_has_titles = []

    expected_title_info = {
         "titles": {
            "main": mock_title_info_main,
            "alternative": mock_title_info_alternative,
            "has_titles": mock_title_info_has_titles
         }
    }

    with patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_pref_lable", return_value=mock_title_info_main), \
        patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_alt_lable", return_value=mock_title_info_alternative), \
        patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_has_titles", return_value=mock_title_info_has_titles):
        
        response = ParseWork.get_title(g, mock_work_id)
        
        assert response == expected_title_info


def test_get_pref_lable():

    mock_work_id = MOCK_WORK_ID

    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)

    expected_pref_lable = {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}

    response = ParseWork.get_pref_lable(g, mock_work_id)

    assert response == expected_pref_lable

def test_get_alt_lable():
    mock_work_id = MOCK_WORK_ID
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)

    expected_alt_lable = [{'text': 'འཕགས་པ་མདོ་སྡུད་པ།', 'code': 'bo'}, {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཡན་ཏ་རིན་པོ་ཆེ་སྡུད་པ།', 'code': 'bo'}, {'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཡོན་ཏན་རིན་པོ་ཆེ་སྡུད་པ།', 'code': 'bo'}, {'text': 'བཅོམ་ལྡན་འདས་མ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, {'text': 'མདོ་སྡུད་པ།', 'code': 'bo'}, {'text': 'སྡུད་པ་ཚིགས་སུ་བཅད་པ།', 'code': 'bo'}, {'text': 'ᠬᠣᠳᠣᠬ ᠳᠣ ᠪᠢᠯᠢᠺ\u202fᠦᠨ ᠴᠢᠨᠠᠳᠣ ᠭᠢᠵᠠᠭᠠᠷ\u180eᠠ ᠭᠥᠷᠥᠭᠰᠡᠨ ᠬᠣᠷᠢᠶᠠᠩᠭᠣᠢ ᠰᠢᠯᠥᠭ', 'code': 'cmg-Mong'}, {'text': 'qutug tu bilig ün cinadu kijagar a kürügsen quriyanggui silüg', 'code': 'cmg-x-poppe'}]

    with patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_alt_lable", return_value=expected_alt_lable):
        response = ParseWork.get_alt_lable(g, mock_work_id)

    assert response == expected_alt_lable

def test_get_has_titles():
    mock_work_id = MOCK_WORK_ID
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()
    
    g = get_graph_for_test(mock_ttl_file, mock_work_id)
    
    expected_has_titles = []
    
    with patch("RDF_to_Neo4j.work.parse_work.ParseWork.get_has_titles", return_value=expected_has_titles):
        response = ParseWork.get_has_titles(g, mock_work_id)
        
    assert response == expected_has_titles

def test_get_language():
    mock_work_id = MOCK_WORK_ID
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_file = f.read()

    g = get_graph_for_test(mock_ttl_file, mock_work_id)
    
    expected_language = {'languages': ['bo']}

    mock_language_id = "LangBo"

    with patch("RDF_to_Neo4j.work.parse_work.PersonUtils.get_id", return_value=mock_language_id):
        response = ParseWork.get_language(g, mock_work_id)
        
    assert response == expected_language

     
