import math
from dataclasses import dataclass
from io import BytesIO
from typing import Tuple

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

IMAGE_MODE = "RGBA"


@dataclass(frozen=True)
class CroppingParameters:
    """
    Parameters for cropping image.

    :param left: indent from left (can be negative)
    :type left: int
    :param top: indent from top (can be negative)
    :type top: int
    :param width: width frame for crop (positive)
    :type width: int
    :param height: height frame for crop (positive)
    :type height: int
    :param scale: scale for base image (positive)
    :type scale: float
    :param background_color: RGB background color
    :type background_color: Tuple[int, int, int]
    """

    left: int
    top: int
    width: int
    height: int
    scale: float
    background_color: Tuple[int, int, int] = (255, 255, 255)

    def get_area(self) -> Tuple[int, int]:
        """Getting area for crop."""
        return -self.left, -self.top


def crop_image(
    file_object: InMemoryUploadedFile,
    parameters: CroppingParameters,  # noqa: WPS110
) -> InMemoryUploadedFile:
    """
    Cropping image by parameters.

    :param file_object: Source file for cropping
    :type file_object: InMemoryUploadedFile
    :param parameters: Parameters for cropping
    :type parameters: CroppingParameters
    :return: Cropped image with inner parameters
    :rtype: InMemoryUploadedFile
    """
    area_image = Image.new(
        IMAGE_MODE,
        (parameters.width, parameters.height),
        parameters.background_color,
    )

    image = Image.open(file_object).convert(IMAGE_MODE)

    if not math.isclose(parameters.scale, 1.0):
        image = image.resize(
            tuple(
                round(dimension * parameters.scale) for dimension in image.size
            ),
        )

    area_image.paste(image, parameters.get_area(), image)

    output = BytesIO()
    area_image.save(output, format="png", quality=100)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        file_object.field_name,
        file_object.name,
        file_object.content_type,
        output.getbuffer().nbytes,
        file_object.charset,
    )
