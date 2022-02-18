import abc

from apps.media.models import File


class IExternalFilesService(abc.ABC):
    """Service for download external files."""

    @abc.abstractmethod
    def download_file_from_url(self, file_url: str, title: str = "") -> File:
        """Download and create file from url."""
