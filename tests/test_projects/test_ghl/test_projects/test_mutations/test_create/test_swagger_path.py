from apps.projects.models import Project


def test_basic(user, ghl_client, couchdb_service, ghl_raw):
    """Test create raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("create_project"),
        variable_values={
            "input": {
                "title": "my project",
                "fromSwagger": {"schemeUrl": "http://swagger.com/my-api.json"},
            },
        },
    )

    project = Project.objects.filter(title="my project").first()
    assert project is not None
    assert project.owner == user

    dto = response["data"]["createProject"]["project"]
    assert dto["title"] == "my project"
    assert couchdb_service.create_database_called
