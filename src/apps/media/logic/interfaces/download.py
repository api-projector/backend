import abc
import io


class IDownloadService(abc.ABC):
    """Service for download external files."""

    @abc.abstractmethod
    def download(self, file_url: str) -> io.BytesIO | None:
        """Download and create file from url."""
