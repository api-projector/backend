from http import HTTPStatus


def test_success(client, project, couchdb_service):
    """Test success."""
    response = client.get(
        "/projects/{0}/export/openapi.json".format(project.id),
    )

    assert response.status_code == HTTPStatus.OK
    assert response["content-type"] == "application/json"
    response_content = response.json()
    assert response_content["info"]["title"] == project.title
    assert not response_content["paths"]
    assert not response_content["components"]["schemas"]


def test_project_not_found(client, project, couchdb_service):
    """Test not found."""
    response = client.get(
        "/projects/{0}bla/export/openapi.json".format(project.id),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
