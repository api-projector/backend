import abc

from django.db import models


class ICleanupMediaFilesService(abc.ABC):
    """Cleanup media files service interface."""

    @abc.abstractmethod
    def cleanup_media_files(self, instance: models.Model) -> None:
        """Cleanup media files."""
