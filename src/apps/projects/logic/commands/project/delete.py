from dataclasses import dataclass

from rest_framework import serializers

from apps.core.logic import messages
from apps.core.logic.helpers.validation import validate_input
from apps.projects.models import Project
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Command result."""


@dataclass(frozen=True)
class ProjectDeleteData:
    """Delete project data."""

    project: str


class Command(messages.BaseCommand[CommandResult]):
    """Delete project command."""

    data: ProjectDeleteData  # noqa: WPS110
    user: User


class _DataValidator(serializers.Serializer):
    """Delete project input."""

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects)


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Deleting projects."""

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            _DataValidator,
        )
        validated_data["project"].delete()

        return CommandResult()
