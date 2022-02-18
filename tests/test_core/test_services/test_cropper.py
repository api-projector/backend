from sys import getsizeof

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from apps.core.services.image.cropper import CroppingParameters, crop_image
from tests.test_media.factories.image import ImageFactory


def test_crop_image(assets):
    """Test cropping image."""
    cropped = crop_image(
        _get_in_memory(assets, "image.jpg"),
        CroppingParameters(left=0, top=0, width=20, height=20, scale=1),
    )

    assert isinstance(cropped, InMemoryUploadedFile)
    assert Image.open(cropped).size == (20, 20)


@pytest.mark.parametrize(  # noqa: PT007
    ("left", "top", "width", "height", "scale"),
    (
        (0, 320, 320, 320, 0.5),
        (640, 650, 640, 650, 1),
        (1280, 650, 640, 650, 1),
        (-100, -100, 640, 640, 0.5),
    ),
)
def test_cropper_upload(  # noqa: WPS211
    user,
    assets,
    left,
    top,
    width,
    height,
    scale,
):
    """Test cropping with different parameters."""
    cropped = crop_image(
        _get_in_memory(assets, "original_image.jpg"),
        CroppingParameters(
            left=left,
            top=top,
            width=width,
            height=height,
            scale=scale,
        ),
    )
    image = ImageFactory()
    image.storage_image = cropped
    image.save()

    path = image.storage_image.path
    target_file = "{0}_{1}_{2}_{3}_{4}.jpg".format(
        left,
        top,
        width,
        height,
        scale,
    )

    assert assets.get_hash(path) == assets.get_hash(target_file)


def _get_in_memory(assets, filename) -> InMemoryUploadedFile:
    """Getting image wrapped to memory uploaded file."""
    image = assets.open_file(filename)

    return InMemoryUploadedFile(
        image,
        "image",
        "image.jpg",
        "image/jpeg",
        getsizeof(image),
        None,
    )
