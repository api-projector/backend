from tests.test_projects.test_logic.test_services.test_projects.test_openapi.asserts import (  # noqa: E501
    assert_paths,
)


def test_many(client, project, couchdb_service, openapi_service, assets):
    """Test path not at spec."""
    docs = assets.read_json("paths")
    couchdb_service.set_documents(docs)

    scheme = openapi_service.get_schema(project)

    assert not scheme["components"]["schemas"]
    assert_paths(
        scheme,
        [doc for key, doc in docs.items() if key in {"1", "2", "3"}],
    )


def test_not_at_spec(
    client,
    project,
    couchdb_service,
    openapi_service,
    assets,
):
    """Test path not at spec."""
    docs = assets.read_json("paths")
    docs["spec"]["paths"] = docs["spec"]["paths"][:2]
    couchdb_service.set_documents(docs)

    scheme = openapi_service.get_schema(project)

    assert not scheme["components"]["schemas"]
    assert_paths(
        scheme,
        [doc for key, doc in docs.items() if key in {"1", "2"}],
    )
