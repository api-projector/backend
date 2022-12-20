from social_core.backends.google import GoogleOAuth2 as SocialGoogleOAuth2

from apps.users.logic.services.signup import SocialSignupData
from apps.users.models import User
from apps.users.services.auth_backends.mixin import OAuth2BackendMixin


class GoogleOAuth2Backend(OAuth2BackendMixin, SocialGoogleOAuth2):
    """Google OAuth authentication backend."""

    def find_user(self, response):
        """Find user for response."""
        return User.objects.filter(email=response["email"]).first()

    def get_signup_data(self, response) -> SocialSignupData:
        """Return data for signup user."""
        return SocialSignupData(
            email=response["email"],
            first_name=response["given_name"],
            last_name=response["family_name"],
            avatar=response["picture"],
        )
