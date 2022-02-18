from dataclasses import dataclass

from rest_framework import serializers

from apps.core.logic import commands
from apps.core.logic.helpers.validation import validate_input
from apps.projects.models import Project
from apps.users.models import User


@dataclass(frozen=True)
class ProjectDeleteData:
    """Delete project data."""

    project: int


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Delete project command."""

    data: ProjectDeleteData  # noqa: WPS110
    user: User


class _DataValidator(serializers.Serializer):
    """Delete project input."""

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects)


class CommandHandler(commands.ICommandHandler[Command, None]):
    """Deleting projects."""

    def execute(self, command: Command) -> None:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            _DataValidator,
        )
        validated_data["project"].delete()
