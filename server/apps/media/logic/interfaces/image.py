import abc

from apps.media.models import Image


class IImageDownloadService(abc.ABC):
    """Image download service."""

    @abc.abstractmethod
    def download_image(self, inbound_url: str) -> Image | None:
        """Download image from any url."""
