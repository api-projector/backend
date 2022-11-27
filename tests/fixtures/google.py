import httpretty
import pytest
from graphql import GraphQLResolveInfo

from apps.users.services.auth_backends.google_oauth2 import GoogleOAuth2Backend
from tests.helpers.ghl_mock import create_mock_info
from tests.helpers.httpretty_client import HttprettyMock


class GoogleMock(HttprettyMock):
    """Google api mocker."""


@pytest.fixture()
def google_mocker():
    """Provides google api mocker."""
    httpretty.enable(allow_net_connect=False)

    yield GoogleMock()

    httpretty.disable()


@pytest.fixture()
def google_token_request_info(rf) -> GraphQLResolveInfo:
    """Provides gitlab token request info."""
    request = rf.get(GoogleOAuth2Backend.AUTHORIZATION_URL)
    setattr(  # noqa: B010
        request,
        "session",
        {"google-oauth2_state": "google_state"},
    )

    return create_mock_info(context=request)
