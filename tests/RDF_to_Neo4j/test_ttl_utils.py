from unittest.mock import patch, Mock
from RDF_to_Neo4j.ttl_utils import TTLUtils

TTL_URL = "DUMMY_TTL_URL"

def test_get_ttl_success():
    mock_id = "WA0RK0013"
    with open("tests/RDF_to_Neo4j/mock_WA0RK0013.ttl", "r", encoding="utf-8") as f:
        mock_ttl = f.read()

    with patch("RDF_to_Neo4j.ttl_utils.requests.get", return_value=Mock(text=mock_ttl)):
        ttl = TTLUtils.get_ttl(mock_id)
        assert ttl == mock_ttl
