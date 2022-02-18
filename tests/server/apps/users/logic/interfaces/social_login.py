import abc
from enum import Enum

from django.http import HttpRequest

from apps.users.models import Token


class SystemBackend(Enum):
    """System social auth backends."""

    GOOGLE = "google"  # noqa: WPS115


class ISocialLoginService(abc.ABC):
    """Social login service."""

    @abc.abstractmethod
    def begin_login(self, request: HttpRequest, system: SystemBackend) -> str:
        """Initial login stage."""

    @abc.abstractmethod
    def complete_login(
        self,
        request: HttpRequest,
        code: str,
        state: str,
        system: SystemBackend,
    ) -> Token:
        """Final login stage."""
