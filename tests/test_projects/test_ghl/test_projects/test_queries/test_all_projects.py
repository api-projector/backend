from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_ALL_PROJECTS = """
query ($sort: [ProjectSort]) {
  allProjects(sort: $sort) {
    count
    edges{
      node{
        id
      }
    }
  }
}
"""


def test_query(user, ghl_client):
    """Test getting all projects raw query."""
    ghl_client.set_user(user)

    ProjectFactory.create_batch(5, owner=user)

    response = ghl_client.execute(GHL_QUERY_ALL_PROJECTS)

    assert "errors" not in response
    assert response["data"]["allProjects"]["count"] == 5


def test_no_owner(ghl_auth_mock_info, all_projects_query):
    """Test success list project."""
    ProjectFactory.create_batch(5)
    response = all_projects_query(root=None, info=ghl_auth_mock_info)

    assert response.length == 0


def test_owner(user, ghl_auth_mock_info, all_projects_query):
    """Test success list project."""
    projects = ProjectFactory.create_batch(5)
    projects[0].owner = user
    projects[0].save()

    response = all_projects_query(root=None, info=ghl_auth_mock_info)

    assert response.length == 1


def test_unauth(ghl_mock_info, all_projects_query, db):
    """Test unauth list project access."""
    ProjectFactory.create_batch(2)

    response = all_projects_query(
        root=None,
        info=ghl_mock_info,
    )

    assert isinstance(response, GraphQLPermissionDenied)
