import io

import requests
from django.core.validators import URLValidator

from apps.media.logic.interfaces.download import IDownloadService


class DownloadService(IDownloadService):
    """Service for download external files."""

    def download(self, file_url: str) -> io.BytesIO | None:
        """Upload file from url."""
        if not file_url:
            raise ValueError("Empty url to download")

        URLValidator()(file_url)
        return self._download_file(file_url)

    def _download_file(self, file_url: str) -> io.BytesIO:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        return io.BytesIO(response.content)
