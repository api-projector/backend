from dataclasses import dataclass

import injector
from django.http import HttpRequest
from django.utils import timezone

from apps.core.logic import messages
from apps.users.logic.interfaces import ISocialLoginService
from apps.users.logic.interfaces.social_login import SystemBackend
from apps.users.models import Token, User


@dataclass(frozen=True)
class CommandResult:
    """Social complete auth output dto."""

    token: Token
    is_new_user: bool


class Command(messages.BaseCommand[CommandResult]):
    """Social login command."""

    request: HttpRequest
    code: str
    state: str
    system: SystemBackend


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Complete social login."""

    @injector.inject
    def __init__(self, social_login_service: ISocialLoginService):
        """Initializing."""
        self._social_login_service = social_login_service

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        token = self._social_login_service.complete_login(
            command.request,
            command.code,
            command.state,
            command.system,
        )

        self._update_user(token.user)

        return CommandResult(
            token=token,
            is_new_user=getattr(token.user, "is_new", False),
        )

    def _update_user(self, user: User):
        user.last_login = timezone.now()
        user.save(update_fields=("last_login",))
