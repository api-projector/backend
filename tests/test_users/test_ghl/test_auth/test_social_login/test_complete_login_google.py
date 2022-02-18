from httpretty import httpretty
from social_core.backends.google import GoogleOAuth2

from apps.users.logic.interfaces.social_login import SystemBackend
from apps.users.models import Token, User

KEY_TOKEN_TYPE = "token_type"  # noqa: S105
KEY_EXPIRES_IN = "expires_in"
KEY_ACCESS_TOKEN = "access_token"  # noqa: S105
KEY_REFRESH_TOKEN = "refresh_token"  # noqa: S105

ACCESS_TOKEN = "access_token"  # noqa: S105
REFRESH_TOKEN = "refresh_token"  # noqa: S105

CREATED_EMAIL = "vasiliy.popov@gitlab.com"


def test_complete_login_in_system(
    user,
    google_mocker,
    social_login_complete_mutation,
    google_token_request_info,
):
    """Test complete login."""
    google_mocker.register_get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        {
            "id": user.pk,
            "given_name": user.first_name,
            "family_name": user.last_name,
            "email": user.email,
        },
    )

    google_mocker.base_api_url = GoogleOAuth2.ACCESS_TOKEN_URL
    google_mocker.register_post(
        "",
        {
            KEY_ACCESS_TOKEN: ACCESS_TOKEN,
            KEY_REFRESH_TOKEN: REFRESH_TOKEN,
            KEY_TOKEN_TYPE: "bearer",
            KEY_EXPIRES_IN: 7200,
        },
    )

    response = social_login_complete_mutation(
        root=None,
        info=google_token_request_info,
        code="test_code",
        state=google_token_request_info.context.session["google-oauth2_state"],
        system=SystemBackend.GOOGLE,
    )

    assert not response.is_new_user
    token = Token.objects.filter(pk=response.token.pk, user=user).first()
    assert token
    assert token.user.last_login


def test_user_not_in_system(
    db,
    google_mocker,
    social_login_complete_mutation,
    google_token_request_info,
    assets,
):
    """Test complete login. User will be created."""
    assert not User.objects.filter(email=CREATED_EMAIL).exists()

    _register_mocks(google_mocker, assets)

    response = social_login_complete_mutation(
        root=None,
        info=google_token_request_info,
        code="test_code",
        state=google_token_request_info.context.session["google-oauth2_state"],
        system=SystemBackend.GOOGLE,
    )

    assert response.is_new_user

    token = Token.objects.get(
        pk=response.token.pk,
        user__email=CREATED_EMAIL,
    )
    assert token.user.avatar
    assert token.user.last_login


def _register_mocks(google_mocker, assets) -> None:
    google_mocker.register_get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        assets.read_json("google_user_response"),
    )
    httpretty.register_uri(
        httpretty.GET,
        "https://lh3.googleusercontent.com/-3OOPP/VV/CC/RR/s96-c/photo.jpg",
        body=assets.open_file("avatar.jpg").read(),
    )

    google_mocker.base_api_url = GoogleOAuth2.ACCESS_TOKEN_URL
    google_mocker.register_post(
        "",
        {
            KEY_ACCESS_TOKEN: ACCESS_TOKEN,
            KEY_REFRESH_TOKEN: REFRESH_TOKEN,
            KEY_TOKEN_TYPE: "bearer",
            KEY_EXPIRES_IN: 7200,
        },
    )
