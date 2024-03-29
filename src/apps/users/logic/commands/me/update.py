from dataclasses import dataclass

from rest_framework import serializers

from apps.core.logic import messages
from apps.users.models import User


class MeUpdateDtoValidator(serializers.Serializer):
    """Update me input validator."""

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)


@dataclass(frozen=True)
class CommandResult:
    """Update me output dto."""

    user: User


class Command(messages.BaseCommand[CommandResult]):
    """Update me."""

    user: User
    first_name: str = ""
    last_name: str = ""


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Update user."""

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        return CommandResult(user=self._update_user(command))

    def _update_user(self, command: Command) -> User:
        """Update user fields from input dto."""
        user_data = command.dict()
        user = user_data.pop("user")

        validator = MeUpdateDtoValidator(data=user_data)
        validator.is_valid(raise_exception=True)

        for field, field_value in validator.validated_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
