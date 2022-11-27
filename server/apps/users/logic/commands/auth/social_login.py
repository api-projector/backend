from dataclasses import dataclass

import injector
from django.http import HttpRequest

from apps.core.logic import messages
from apps.users.logic.interfaces import ISocialLoginService
from apps.users.logic.interfaces.social_login import SystemBackend


@dataclass(frozen=True)
class CommandResult:
    """Login output dto."""

    redirect_url: str


class Command(messages.BaseCommand[CommandResult]):
    """Social login input data."""

    request: HttpRequest
    system: SystemBackend


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Social login."""

    @injector.inject
    def __init__(self, social_login_service: ISocialLoginService):
        """Initializing."""
        self._social_login_service = social_login_service

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        redirect_url = self._social_login_service.begin_login(
            command.request,
            command.system,
        )

        return CommandResult(
            redirect_url=redirect_url,
        )
