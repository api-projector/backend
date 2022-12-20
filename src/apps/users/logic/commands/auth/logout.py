from dataclasses import dataclass

import injector

from apps.core.logic import messages
from apps.users.logic.interfaces import ITokenService
from apps.users.models import Token


@dataclass(frozen=True)
class CommandResult:
    """Command result."""


class Command(messages.BaseCommand[CommandResult]):
    """Logout command."""

    token: Token


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Logout service."""

    @injector.inject
    def __init__(self, token_service: ITokenService):
        """Initializing."""
        self._token_service = token_service

    def handle(self, command: Command) -> CommandResult:
        """Main logic."""
        self._token_service.delete_token(command.token)

        return CommandResult()
