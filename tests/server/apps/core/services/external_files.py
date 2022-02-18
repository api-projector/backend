import logging
from tempfile import TemporaryFile
from typing import Optional

import requests
from django.core.exceptions import ValidationError
from django.core.files import File as DjangoFile
from django.core.validators import URLValidator

from apps.core.logic.interfaces.external_files import IExternalFilesService
from apps.media.models import File

logger = logging.getLogger(__name__)


CHUNK_SIZE = 4096


class ExternalFilesService(IExternalFilesService):
    """Service for download external files."""

    def download_file_from_url(
        self,
        file_url: str,
        title: str = "",
    ) -> Optional[File]:
        """Upload file from url."""
        if not file_url:
            return None

        try:
            URLValidator()(file_url)
        except ValidationError as err:
            logger.warning(err)
            return None

        try:
            return self._download_file(file_url, title)
        except Exception:
            logger.warning("The file wasn't downloaded.")

        return None

    def _download_file(self, file_url, title) -> File:
        instance_file = File()
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        filename = self._get_filename(file_url, title)
        instance_file.original_filename = filename

        with TemporaryFile() as tmp_file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                tmp_file.write(chunk)

            tmp_file.seek(0)
            instance_file.storage_file.save(
                filename,
                DjangoFile(tmp_file),
            )
        instance_file.save()
        return instance_file

    def _get_filename(self, file_url, title) -> str:
        if title:
            return "{0}.png".format(title)
        return file_url.split("/")[-1]
