import typing

from django.core.files.storage import default_storage
from django.db import models

from apps.media.logic.interfaces import ICleanupMediaFilesService
from apps.media.models import Image


class CleanupMediaFilesService(ICleanupMediaFilesService):
    """Cleanup media files service."""

    def cleanup_media_files(self, instance: models.Model) -> None:
        """Cleanup media files."""
        self._cleanup_images(instance)

    def _cleanup_images(self, instance: models.Model) -> None:
        for image_field in self._get_media_fields(instance, Image):
            media_instance = getattr(instance, image_field.name)
            if media_instance:
                self._delete_image(media_instance)

    def _delete_file(self, file_instance: models.Model) -> None:
        self._delete_media_from_storage(file_instance.storage_file)
        file_instance.delete()

    def _delete_image(self, image_instance: models.Model) -> None:
        self._delete_media_from_storage(image_instance.storage_image)
        image_instance.delete()

    def _delete_media_from_storage(
        self,
        media_field: models.FileField,
    ) -> None:
        if media_field and default_storage.exists(media_field.name):
            default_storage.delete(media_field.name)

    def _get_media_fields(
        self,
        instance: models.Model,
        related_model: models.Model,
    ) -> typing.List[models.Field]:
        return [
            field
            for field in instance._meta.get_fields()  # noqa: WPS437
            if field.is_relation
            and not field.auto_created
            and field.related_model == related_model
        ]
