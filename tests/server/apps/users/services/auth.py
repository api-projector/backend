import abc

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError
from apps.users.logic.interfaces import IAuthenticationService
from apps.users.models import User


class LoginError(BaseInfrastructureError, metaclass=abc.ABCMeta):
    """Base class for login errors."""


class AuthenticationError(LoginError):
    """Wrong credentials error."""

    code = "authentication_failed"
    message = _("MSG__UNABLE_TO_LOGIN_WITH_PROVIDED_CREDENTIALS")


class AuthenticationService(IAuthenticationService):
    """Login service."""

    def auth(self, email: str, password: str) -> User:
        """Login user by provided credentials."""
        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationError()

        return user
