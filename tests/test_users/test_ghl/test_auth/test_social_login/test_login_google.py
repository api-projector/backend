import pytest
from django.conf import settings
from social_core.backends.google import GoogleOAuth2

from apps.users.logic.interfaces.social_login import SystemBackend
from tests.helpers.ghl_client import GraphQLClient
from tests.helpers.gql_raw_query_provider import GhlRawQueryProvider


@pytest.fixture(scope="module", autouse=True)
def _google_login() -> None:
    """Forces django to use gitlab settings."""
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = "redirect_uri"
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "test_google_key"
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "test_google_secret"


def test_query(
    ghl_client: GraphQLClient,
    ghl_raw: GhlRawQueryProvider,
) -> None:
    """Test raw query."""
    response = ghl_client.execute(
        ghl_raw("social_login"),
        variable_values={
            "system": SystemBackend.GOOGLE.name,
        },
    )

    assert "errors" not in response
    redirect_url = response["data"]["socialLogin"]["redirectUrl"]

    client = "client_id={0}".format(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
    redirect = "redirect_uri={0}".format(
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
    )

    assert redirect_url.startswith(GoogleOAuth2.AUTHORIZATION_URL)
    assert client in redirect_url
    assert redirect in redirect_url
