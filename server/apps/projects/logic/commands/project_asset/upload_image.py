from dataclasses import dataclass

import injector
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from apps.core.logic import commands
from apps.core.logic.errors import InvalidInputApplicationError
from apps.projects.logic.services.projects.assets import ProjectAssetsService
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource
from apps.users.models import User


class _ProjectAssetDtoValidator(serializers.Serializer):
    """Create project asset input."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )


@dataclass(frozen=True)
class ImageProjectAssetDto:
    """Create image project asset data."""

    file: InMemoryUploadedFile  # noqa: WPS110
    project: str = ""


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Create figma project asset input dto."""

    data: ImageProjectAssetDto  # noqa: WPS110
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
        project_assets_service: ProjectAssetsService,
    ):
        """Initialize."""
        self._project_assets_service = project_assets_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        validator = _ProjectAssetDtoValidator(
            data=(
                {
                    "project": command.data.project,
                }
            ),
        )
        if not validator.is_valid():
            raise InvalidInputApplicationError(validator.errors)

        validated_data = validator.validated_data

        project_asset = self._project_assets_service.add_image_asset(
            project=validated_data["project"],
            filename=command.data.file.name,
            source=ProjectAssetSource.UPLOAD,
            image_source=command.data.file,
        )

        return CommandResult(
            project_asset=project_asset,
        )
