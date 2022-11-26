from apps.projects.models import Project, SwaggerImport
from apps.projects.models.enums import SwaggerImportState
from apps.users.models import User
from tests.helpers.couchdb import StubCouchDBService
from tests.helpers.ghl_client import GraphQLClient
from tests.helpers.gql_raw_query_provider import GhlRawQueryProvider


def test_path(
    user: User,
    ghl_client: GraphQLClient,
    couchdb_service: StubCouchDBService,
    ghl_raw: GhlRawQueryProvider,
) -> None:
    """Test create raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("create_project_swagger"),
        variable_values={
            "input": {
                "title": "my project",
                "fromSwagger": {"schemeUrl": "http://swagger.com/my-api.json"},
            },
        },
    )

    assert "errors" not in response

    project = Project.objects.get(title="my project")
    assert SwaggerImport.objects.count() == 1
    swagger_import = SwaggerImport.objects.first()
    assert swagger_import.project == project
    assert swagger_import.swagger_url == "http://swagger.com/my-api.json"
    assert swagger_import.state == SwaggerImportState.CREATED


def test_job_response(
    user: User,
    ghl_client: GraphQLClient,
    couchdb_service: StubCouchDBService,
    ghl_raw: GhlRawQueryProvider,
) -> None:
    """Test create raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("create_project_swagger"),
        variable_values={
            "input": {
                "title": "my project",
                "fromSwagger": {"schemeUrl": "http://swagger.com/my-api.json"},
            },
        },
    )

    assert "errors" not in response

    dto = response["data"]["createProject"]["project"]
    assert dto["importSwaggerJob"] is not None
    assert dto["importSwaggerJob"]["state"] == SwaggerImportState.CREATED
