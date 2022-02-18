from http import HTTPStatus

from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied
from rest_framework.test import APIClient

from apps.users.models import Token
from apps.users.services import TokenService
from tests.fixtures.users import DEFAULT_EMAIL, DEFAULT_USER_PASSWORD


def test_query(user, ghl_client, ghl_raw):
    """Test logout raw query."""
    ghl_client.set_user(user)

    assert Token.objects.filter(user=user).exists()

    response = ghl_client.execute(ghl_raw("logout"))

    assert "errors" not in response
    assert response["data"]["logout"]["status"] == "success"
    assert not Token.objects.filter(user=user).exists()


def test_api_query(user, ghl_raw):
    """Test raw api query."""
    token_service = TokenService()
    token = token_service.create_user_token(user)

    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {0}".format(token.key))

    query_body = {
        "query": ghl_raw("logout"),
        "variables": {
            "input": {
                "email": DEFAULT_EMAIL,
                "password": DEFAULT_USER_PASSWORD,
            },
        },
    }
    response = api_client.post("/api/graphql", data=query_body, format="json")
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK


def test_success(user, ghl_auth_mock_info, logout_mutation):
    """Test success logout."""
    assert Token.objects.filter(user=user).exists()

    logout_mutation(root=None, info=ghl_auth_mock_info)

    assert not Token.objects.filter(user=user).exists()


def test_non_auth(user, ghl_mock_info, logout_mutation):
    """Test logout if user is not logged."""
    response = logout_mutation(root=None, info=ghl_mock_info)
    assert isinstance(response, GraphQLPermissionDenied)
