from dataclasses import dataclass

import injector

from apps.core.logic import commands
from apps.users.logic.interfaces import ITokenService
from apps.users.models import Token


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Logout command."""

    token: Token


class CommandHandler(commands.ICommandHandler[Command, None]):
    """Logout service."""

    @injector.inject
    def __init__(self, token_service: ITokenService):
        """Initializing."""
        self._token_service = token_service

    def execute(self, command: Command) -> None:
        """Main logic."""
        self._token_service.delete_token(command.token)
