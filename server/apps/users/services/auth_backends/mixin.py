from django.http import HttpResponseBadRequest
from django.utils import timezone
from social_core.backends.oauth import BaseOAuth2
from social_core.utils import handle_http_errors

from apps.core import injector
from apps.users.logic.interfaces import ITokenService
from apps.users.logic.interfaces.signup import ISignupService, SocialSignupData
from apps.users.models import User


class OAuth2BackendMixin(BaseOAuth2):
    """Common oauth2 backend logic."""

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Do Google OAuth and return token."""
        user = super().auth_complete(*args, **kwargs)

        if not user:
            return HttpResponseBadRequest("Invalid token")

        token_service = injector.get(ITokenService)
        token = token_service.create_user_token(user)

        user.last_login = timezone.now()
        user.save(update_fields=("last_login",))

        return token  # noqa: WPS331

    def authenticate(self, *args, **kwargs) -> User | None:
        """Return authenticated user."""
        if not self._backend_valid(**kwargs):
            return None

        response = kwargs["response"]

        user = self.find_user(response)
        if user:
            return user

        signup_service = injector.get(ISignupService)
        user = signup_service.signup_from_social(
            self.get_signup_data(response),
        )

        user.is_new = True
        return user

    def find_user(self, response) -> User | None:
        """Find user for response."""
        raise NotImplementedError()

    def get_signup_data(self, response) -> SocialSignupData:
        """Return data for signup user."""
        raise NotImplementedError()

    def get_redirect_uri(self, state=None):
        """Callback URL after approving access on Google."""
        return self.setting("REDIRECT_URI")

    def set_data(self, **kwargs):  # noqa: WPS615
        """Set data."""
        self.data = kwargs  # noqa: WPS110

    def _backend_valid(self, **kwargs) -> bool:
        required_fields = ("backend", "strategy", "response")
        for required_field in required_fields:
            if required_field not in kwargs:
                return False

        return kwargs["backend"].name == self.name
