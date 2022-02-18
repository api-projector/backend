from django.core.files.storage import default_storage
from PIL import Image as PilImage

from apps.media.models import Image


def test_upload_image(
    user,
    ghl_auth_mock_info,
    upload_image_mutation,
    in_memory_uploaded,
):
    """Test upload image."""
    ghl_auth_mock_info.context.FILES[0] = in_memory_uploaded

    width, height = 10, 15

    assert not Image.objects.exists()

    response = upload_image_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "file": in_memory_uploaded,
            "left": 0,
            "top": 0,
            "width": width,
            "height": height,
            "scale": 1,
        },
    )

    assert Image.objects.get(original_filename=in_memory_uploaded.name)

    opened_image = PilImage.open(
        default_storage.open(response.image.storage_image.name),
    )
    assert opened_image.size == (width, height)
