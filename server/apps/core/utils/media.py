from django.conf import settings
from django.db import models


def get_absolute_path(file_field: models.FileField) -> str:
    """Generate absolute file path."""
    if file_field:
        return "https://{0}{1}{2}".format(
            settings.DOMAIN_NAME,
            settings.MEDIA_URL,
            file_field.name,
        )

    return file_field
