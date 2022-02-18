from dataclasses import asdict, dataclass

from rest_framework import serializers

from apps.core.logic import commands
from apps.users.models import User


class MeUpdateDtoValidator(serializers.Serializer):
    """Update me input validator."""

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Update me."""

    user: User
    first_name: str = ""
    last_name: str = ""


@dataclass(frozen=True)
class CommandResult:
    """Update me output dto."""

    user: User


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Update user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        return CommandResult(user=self._update_user(command))

    def _update_user(self, command: Command) -> User:
        """Update user fields from input dto."""
        user_data = asdict(command)
        user = user_data.pop("user")

        validator = MeUpdateDtoValidator(data=user_data)
        validator.is_valid(raise_exception=True)

        for field, field_value in validator.validated_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
