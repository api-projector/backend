from jnt_django_graphene_toolbox.errors import GraphQLNotFound

from tests.test_projects.factories.project import ProjectFactory


def test_query(user, ghl_client, ghl_raw):
    """Test getting project raw query."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)

    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )

    assert "errors" not in response
    assert response["data"]["project"]["id"] == str(project.id)


def test_owner(ghl_auth_mock_info, project_query):
    """Test success getting project when owner."""
    project = ProjectFactory.create(owner=ghl_auth_mock_info.context.user)
    response = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id=project.id,
    )

    assert response == project


def test_not_owner(ghl_auth_mock_info, project_query):
    """Test success getting project when not owner."""
    project = ProjectFactory.create()
    response = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id=project.id,
    )

    assert response == project


def test_not_found(ghl_auth_mock_info, project_query):
    """Test project not found."""
    ProjectFactory.create()

    response = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id="1",
    )
    assert isinstance(response, GraphQLNotFound)


def test_unauth(ghl_mock_info, project_query, db):
    """Test non authorized user."""
    project = ProjectFactory.create()

    response = project_query(root=None, info=ghl_mock_info, id=project.id)

    assert isinstance(response, GraphQLNotFound)
