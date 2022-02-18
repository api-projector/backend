def test_info(client, project, couchdb_service, openapi_service):
    """Test info."""
    scheme = openapi_service.get_schema(project)

    assert scheme["info"]["title"] == project.title
    assert scheme["info"]["version"] == "v1"
    assert scheme["openapi"] == "3.0.3"


def test_empty(client, project, couchdb_service, openapi_service):
    """Test empty."""
    scheme = openapi_service.get_schema(project)

    assert not scheme["paths"]
    assert not scheme["components"]["schemas"]
