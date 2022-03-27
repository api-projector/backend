import io

from django.core.files import File as DjangoFile

from apps.media.models import File
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource


class ProjectAssetsService:
    """Project assets manager."""

    def add_image_asset(
        self,
        project: Project,
        filename: str,
        source: ProjectAssetSource,
        image_source: DjangoFile | io.BytesIO,
    ) -> ProjectAsset:
        """Add project asset to project."""
        instance_file = File()
        instance_file.original_filename = filename
        instance_file.storage_file.save(
            filename,
            image_source,
        )
        instance_file.save()

        return ProjectAsset.objects.create(
            project=project,
            source=source,
            file=instance_file,
        )
