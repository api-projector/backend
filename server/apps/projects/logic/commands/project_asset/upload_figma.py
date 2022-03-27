import io
from dataclasses import dataclass

import injector
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core.logic import commands, errors
from apps.core.logic.helpers.validation import validate_input
from apps.media.logic.interfaces import IExternalFilesService
from apps.projects.logic.interfaces import IFigmaService, IFigmaServiceFactory
from apps.projects.logic.services.projects.assets import ProjectAssetsService
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource
from apps.users.models import User


class ImageNotDownloadedError(errors.BaseApplicationError):
    """Mark the error as not_found error."""

    code = "image_not_downloaded"
    message = _("MSG__CANNOT_DOWNLOAD_FIGMA_IMAGE")


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
        project_assets_service: ProjectAssetsService,
    ):
        """Initialize."""
        self._figma_service_factory = figma_service_factory
        self._external_files_service = external_files_service
        self._project_assets_service = project_assets_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            _ProjectAssetDtoValidator,
        )

        project_asset = self._create_project_asset(
            validated_data["project"],
            validated_data["url"],
        )

        return CommandResult(
            project_asset=project_asset,
        )

    def _create_project_asset(
        self,
        project: Project,
        url: str,
    ) -> ProjectAsset:
        figma_service = self._figma_service_factory.create(project)

        figma_file = self._download_file(url, figma_service)

        image_params = figma_service.get_image_params(url)

        filename = self._get_filename(url, image_params.title)
        return self._project_assets_service.add_image_asset(
            project=project,
            filename=filename,
            source=ProjectAssetSource.FIGMA,
            image_source=figma_file,
        )

    def _download_file(
        self,
        url: str,
        figma_service: IFigmaService,
    ) -> io.BytesIO:
        image_url = figma_service.get_image_url(url)
        downloaded_file = self._external_files_service.download_file_from_url(
            image_url,
        )

        if not downloaded_file:
            raise ImageNotDownloadedError()

        return downloaded_file

    def _get_filename(self, file_url: str, title: str) -> str:
        if title:
            return "{0}.png".format(title)
        return file_url.split("/")[-1]
