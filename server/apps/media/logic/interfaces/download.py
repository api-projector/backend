import abc
import io
import typing as ty


class IDownloadService(abc.ABC):
    """Service for download external files."""

    @abc.abstractmethod
    def download(self, file_url: str) -> ty.Optional[io.BytesIO]:
        """Download and create file from url."""
