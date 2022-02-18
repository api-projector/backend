from dataclasses import dataclass

import injector

from apps.core.logic import commands
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.interfaces import ICouchDBService
from apps.core.utils.objects import empty
from apps.projects.logic.commands.project.create import dto
from apps.projects.models import FigmaIntegration, Project
from apps.users.models import User


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Create project input dto."""

    data: dto.ProjectDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class CommandResult:
    """Create project output dto."""

    project: Project


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Creating projects."""

    @injector.inject
    def __init__(
        self,
        couch_db_service: ICouchDBService,
    ):
        """Initialize."""
        self._couch_db_service = couch_db_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            dto.ProjectDtoValidator,
        )

        project = Project.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            owner=command.user,
            emblem=validated_data.get("emblem"),
        )

        self._add_figma_integration(project, validated_data)

        self._couch_db_service.create_database(project.db_name)

        return CommandResult(project=project)

    def _add_figma_integration(self, project: Project, validated_data) -> None:
        integration = validated_data.get("figma_integration")
        if integration and integration != empty:
            FigmaIntegration.objects.create(
                project=project,
                token=integration["token"],
            )
