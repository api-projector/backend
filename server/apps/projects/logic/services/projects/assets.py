import io
import os

import injector
from django.core.files import File as DjangoFile

from apps.media.logic.interfaces import IImageConverter
from apps.media.models import File
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource

PROJECT_ASSET_QUALITY = 80


class ProjectAssetsService:
    """Project assets manager."""

    @injector.inject
    def __init__(self, image_converter: IImageConverter):
        """Initialize."""
        self._image_converter = image_converter

    def add_image_asset(
        self,
        project: Project,
        filename: str,
        source: ProjectAssetSource,
        image: DjangoFile | io.BytesIO,
    ) -> ProjectAsset:
        """Add project asset to project."""
        instance_file = File()
        instance_file.original_filename = filename

        converted = self._image_converter.convert_to_webp(
            image,
            quality=PROJECT_ASSET_QUALITY,
        )

        instance_file.storage_file.save(
            "{0}.webp".format(os.path.splitext(filename)[0]),
            converted,
        )
        instance_file.save()

        return ProjectAsset.objects.create(
            project=project,
            source=source,
            file=instance_file,
        )
