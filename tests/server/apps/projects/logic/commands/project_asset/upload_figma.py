from dataclasses import dataclass

import injector
from rest_framework import serializers

from apps.core.logic import commands
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.interfaces import IExternalFilesService
from apps.media.models import File
from apps.projects.logic.interfaces import IFigmaServiceFactory
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource
from apps.users.models import User


class _ProjectAssetDtoValidator(serializers.Serializer):
    """Create project asset input."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )
    url = serializers.CharField()


@dataclass(frozen=True)
class FigmaProjectAssetDto:
    """Create figma project asset data."""

    project: str = ""
    url: str = ""


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Create figma project asset input dto."""

    data: FigmaProjectAssetDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class CommandResult:
    """Create project output."""

    project_asset: ProjectAsset


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Create project asset."""

    @injector.inject
    def __init__(
        self,
        figma_service_factory: IFigmaServiceFactory,
        external_files_service: IExternalFilesService,
    ):
        """Initialize."""
        self._figma_service_factory = figma_service_factory
        self._external_files_service = external_files_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            _ProjectAssetDtoValidator,
        )

        project_asset = ProjectAsset.objects.create(
            project=validated_data["project"],
            source=ProjectAssetSource.FIGMA,
        )

        project_asset.file = self._download_file(
            validated_data["url"],
            project_asset,
        )
        project_asset.save()

        return CommandResult(
            project_asset=project_asset,
        )

    def _download_file(
        self,
        url: str,
        project_asset: ProjectAsset,
    ) -> File:
        """Download file."""
        figma_service = self._figma_service_factory.create(
            project_asset.project,
        )
        image_params = figma_service.get_image_params(url)
        image_url = figma_service.get_image_url(url)

        return self._external_files_service.download_file_from_url(
            image_url,
            image_params.title,
        )
