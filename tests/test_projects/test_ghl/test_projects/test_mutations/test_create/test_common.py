from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)

from apps.projects.models import Project
from tests.test_media.factories.image import ImageFactory


def test_query(user, ghl_client, couchdb_service, ghl_raw):
    """Test create raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("create_project"),
        variable_values={
            "input": {"title": "my project"},
        },
    )

    project = Project.objects.filter(title="my project").first()
    assert project is not None
    assert project.owner == user

    dto = response["data"]["createProject"]["project"]
    assert dto["title"] == "my project"
    assert couchdb_service.create_database_called


def test_success(
    user,
    ghl_auth_mock_info,
    create_project_mutation,
    couchdb_service,
):
    """Test success create."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "title": "my project",
            "description": "description",
            "emblem": ImageFactory.create().pk,
        },
    )

    assert response.project.owner == user
    assert response.project.description == "description"
    assert response.project.emblem
    assert couchdb_service.create_database_called


def test_unauth(user, ghl_mock_info, create_project_mutation):
    """Test unauthorized access."""
    response = create_project_mutation(
        root=None,
        info=ghl_mock_info,
        input={
            "title": "my project",
        },
    )

    assert isinstance(response, GraphQLPermissionDenied)


def test_empty_title(
    user,
    ghl_auth_mock_info,
    create_project_mutation,
    couchdb_service,
):
    """Test bad input data."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "title": "",
        },
    )

    assert isinstance(response, GraphQLInputError)
    assert not Project.objects.exists()


def test_integration(
    user,
    ghl_auth_mock_info,
    create_project_mutation,
    couchdb_service,
):
    """Test integration data."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "title": "project",
            "figma_integration": {"token": "super token"},
        },
    )

    integration = response.project.figma_integration
    assert integration
    assert integration.token == "super token"
