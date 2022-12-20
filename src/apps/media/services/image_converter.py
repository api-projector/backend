import io

from PIL import Image

from apps.media.logic.interfaces import IImageConverter


class ImageConverter(IImageConverter):
    """Service for images convertion."""

    def convert_to_webp(self, image, quality: int) -> io.BytesIO:
        """Convert image to WebP format."""
        pil_image = Image.open(image)
        image_bytes = io.BytesIO()
        pil_image.save(image_bytes, "WEBP")
        return image_bytes
