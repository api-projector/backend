import logging
import os
import pathlib
import tempfile
from typing import Optional

import requests
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import URLValidator

from apps.media.logic.interfaces import IImageDownloadService
from apps.media.models import Image

logger = logging.getLogger(__name__)


class ImageDownloadService(IImageDownloadService):
    """Image service."""

    def download_image_from_url(self, image_link: str) -> Optional[Image]:
        """Download image from url."""
        if not image_link:
            return None

        try:
            URLValidator()(image_link)
        except ValidationError as err:
            logger.warning(err)
            return None

        try:
            return self._download_image(image_link)
        except Exception:
            logger.warning("The picture wasn't downloaded.")

        return None

    def _download_image(self, image_link: str) -> Image:
        instance_image = Image()

        response = requests.get(image_link, stream=True)
        response.raise_for_status()

        suffix = pathlib.Path(response.url).suffix
        with tempfile.TemporaryFile(suffix=suffix) as tmp_file:
            for chunk in response.iter_content(1024):
                tmp_file.write(chunk)
            instance_image.storage_image.save(
                os.path.basename(response.url),
                File(tmp_file),
                save=True,
            )
        return instance_image
