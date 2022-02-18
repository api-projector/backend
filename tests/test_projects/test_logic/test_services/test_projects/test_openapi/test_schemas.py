from tests.test_projects.test_logic.test_services.test_projects.test_openapi.asserts import (  # noqa: E501
    assert_schemas,
)


def test_many(client, project, couchdb_service, openapi_service, assets):
    """Test many schemas."""
    docs = assets.read_json("schemas")
    couchdb_service.set_documents(docs)

    scheme = openapi_service.get_schema(project)

    assert not scheme["paths"]
    assert_schemas(
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
    """Test schema not at spec."""
    docs = assets.read_json("schemas")
    docs["spec"]["schemas"] = docs["spec"]["schemas"][:2]
    couchdb_service.set_documents(docs)

    scheme = openapi_service.get_schema(project)

    assert not scheme["paths"]
    assert_schemas(
        scheme,
        [doc for key, doc in docs.items() if key in {"1", "2"}],
    )
