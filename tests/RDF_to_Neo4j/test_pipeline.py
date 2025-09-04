from unittest.mock import patch

from RDF_to_Neo4j.pipeline import pipeline


def test_pipeline():
    mock_work_id = "WA0RK0013"
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl_content = f.read()

    mock_work_info = {
        'expression_bdrc': 'WA0RK0013',
        'title': {
            'titles': {
                'main': {
                    'text': 'འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་སྡུད་པ་ཚིགས་སུ་བཅད་པ།',
                    'code': 'bo'
                }
            }
        }
    }

    with patch("RDF_to_Neo4j.pipeline.TTLUtils.get_ttl", return_value=mock_ttl_content) as mock_get_ttl, \
         patch("RDF_to_Neo4j.pipeline.ParseWork.parse_work_ttl", return_value=mock_work_info) as mock_parse, \
         patch("RDF_to_Neo4j.pipeline.FileOperationUtils.write_json") as mock_write_json:

        pipeline(mock_work_id)

        mock_get_ttl.assert_called_once_with(mock_work_id)
        mock_parse.assert_called_once_with(mock_ttl_content, mock_work_id)
        mock_write_json.assert_called_once_with(data=mock_work_info, file_name=mock_work_id)
