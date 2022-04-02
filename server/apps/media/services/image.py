import os
from typing import Optional

import injector
from django.core.files import File

from apps.media.logic.interfaces import IDownloadService, IImageDownloadService
from apps.media.models import Image


class ImageDownloadService(IImageDownloadService):
    """Image service."""

    @injector.inject
    def __init__(self, download_service: IDownloadService):
        """Initialize."""
        self._download_service = download_service

    def download_image(self, image_link: str) -> Optional[Image]:
        """Download image from url."""
        raw_data = self._download_service.download(image_link)
        if not raw_data:
            return None

        image = Image()
        image.original_filename = os.path.basename(image_link)
        image.storage_image.save(
            image.original_filename,
            File(raw_data),
            save=True,
        )

        return image
