import io
import logging

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from apps.media.logic.interfaces.download import IDownloadService

logger = logging.getLogger(__name__)


class DownloadService(IDownloadService):
    """Service for download external files."""

    def download(self, file_url: str) -> io.BytesIO | None:
        """Upload file from url."""
        if not file_url:
            return None

        try:
            URLValidator()(file_url)
        except ValidationError as err:
            logger.warning(err)
            return None

        try:
            return self._download_file(file_url)
        except requests.HTTPError:
            logger.warning("The file wasn't downloaded.")

        return None

    def _download_file(self, file_url: str) -> io.BytesIO:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        return io.BytesIO(response.content)
