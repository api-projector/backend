from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from apps.core.logic import commands
from apps.core.logic.errors import InvalidInputApplicationError
from apps.media.models import File
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

        instance_file = File()
        instance_file.original_filename = command.data.file.name
        instance_file.storage_file.save(
            command.data.file.name,
            command.data.file,
        )
        instance_file.save()

        project_asset = ProjectAsset.objects.create(
            project=validated_data["project"],
            source=ProjectAssetSource.UPLOAD,
            file=instance_file,
        )

        return CommandResult(
            project_asset=project_asset,
        )
