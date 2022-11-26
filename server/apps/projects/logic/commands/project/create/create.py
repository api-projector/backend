from dataclasses import dataclass

import injector

from apps.core.helpers.objects import empty
from apps.core.logic import messages
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.interfaces import ICouchDBService
from apps.projects.logic.commands.project import import_swagger
from apps.projects.logic.commands.project.create import dto
from apps.projects.models import FigmaIntegration, Project, SwaggerImport
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Create project output dto."""

    project: Project


@dataclass(frozen=True)
class SwaggerSource:
    """Swagger data."""

    scheme_url: str | None


class Command(messages.BaseCommand[CommandResult]):
    """Create project input dto."""

    data: dto.ProjectDto  # noqa: WPS110
    user: User
    swagger_source: SwaggerSource | None = None


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Creating projects."""

    @injector.inject
    def __init__(
        self,
        couch_db_service: ICouchDBService,
    ):
        """Initialize."""
        self._couch_db_service = couch_db_service

    def handle(self, command: Command) -> CommandResult:
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

        if command.swagger_source:
            self._import_swagger(command.swagger_source, project)

        return CommandResult(project=project)

    def _add_figma_integration(self, project: Project, validated_data) -> None:
        integration = validated_data.get("figma_integration")
        if integration and integration != empty:
            FigmaIntegration.objects.create(
                project=project,
                token=integration["token"],
            )

    def _import_swagger(
        self,
        source: SwaggerSource,
        project: Project,
    ) -> None:
        swagger_import = SwaggerImport.objects.create(
            project=project,
            swagger_url=source.scheme_url,
        )

        messages.dispatch_message_async(
            import_swagger.Command(
                swagger_import_id=swagger_import.id,
            ),
        )
