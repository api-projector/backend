import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

IMAGE_FILE = "image.jpg"


@pytest.fixture()
def in_memory_uploaded(assets):
    """Wrap image to in memory."""
    image = assets.open_file(IMAGE_FILE)
    return InMemoryUploadedFile(
        image,
        "image",
        "middle.jpeg",
        "image/jpeg",
        42,
        "utf-8",
    )
