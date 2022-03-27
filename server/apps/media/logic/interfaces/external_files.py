import abc
import io
import typing as ty


class IExternalFilesService(abc.ABC):
    """Service for download external files."""

    @abc.abstractmethod
    def download_file_from_url(self, file_url: str) -> ty.Optional[io.BytesIO]:
        """Download and create file from url."""
