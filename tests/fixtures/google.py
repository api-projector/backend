import httpretty
import pytest
from graphene_django.rest_framework.tests.test_mutation import mock_info
from graphql import ResolveInfo

from apps.users.services.auth_backends.google_oauth2 import GoogleOAuth2Backend
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
def google_token_request_info(rf) -> ResolveInfo:
    """Provides gitlab token request info."""
    request = rf.get(GoogleOAuth2Backend.AUTHORIZATION_URL)
    setattr(  # noqa: B010
        request,
        "session",
        {"google-oauth2_state": "google_state"},
    )

    resolve_info = mock_info()
    resolve_info.context = request

    return resolve_info
