from RDF_to_Neo4j.parse_instance import add_one


def test_add_one():
    assert add_one(1) == 2
