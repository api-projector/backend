import abc
import io


class IImageConverter(abc.ABC):
    """Service for images convertion."""

    @abc.abstractmethod
    def convert_to_webp(self, image, quality: int) -> io.BytesIO:
        """Convert image to WebP format."""
