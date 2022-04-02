import abc
from typing import Optional

from apps.media.models import Image


class IImageDownloadService(abc.ABC):
    """Image download service."""

    @abc.abstractmethod
    def download_image(self, inbound_url: str) -> Optional[Image]:
        """Download image from any url."""
