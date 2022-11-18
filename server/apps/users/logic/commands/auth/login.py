import abc
from dataclasses import dataclass

import injector
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.logic import messages
from apps.core.logic.errors import BaseApplicationError
from apps.core.services.errors import BaseInfrastructureError
from apps.users.logic.interfaces import IAuthenticationService, ITokenService
from apps.users.models import Token, User


@dataclass(frozen=True)
class CommandResult:
    """Login command result."""

    token: Token


class Command(messages.BaseCommand[CommandResult]):
    """Login command."""

    email: str
    password: str


class LoginError(BaseApplicationError, metaclass=abc.ABCMeta):
    """Generic login error."""


class EmptyCredentialsError(LoginError):
    """Empty credentials error."""

    code = "empty_credentials"
    message = _("MSG__MUST_INCLUDE_EMAIL_AND_PASSWORD")


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Login command handler."""

    @injector.inject
    def __init__(
        self,
        auth_service: IAuthenticationService,
        token_service: ITokenService,
    ):
        """Initializing."""
        self._auth_service = auth_service
        self._token_service = token_service

    def handle(self, command: Command) -> CommandResult:
        """Handle command."""
        self._validate_command(command)

        try:
            user = self._auth_service.auth(
                command.email,
                command.password,
            )
        except BaseInfrastructureError as err:
            raise LoginError(err.code, str(err))

        self._update_user(user)

        return CommandResult(
            token=self._token_service.create_user_token(user),
        )

    def _validate_command(self, command: Command) -> None:
        if not command.email or not command.password:
            raise EmptyCredentialsError()

    def _update_user(self, user: User):
        user.last_login = timezone.now()
        user.save(update_fields=("last_login",))
