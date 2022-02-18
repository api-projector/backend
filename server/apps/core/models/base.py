from django.db import models
from django.dispatch import receiver


class BaseModel(models.Model):
    """Base model."""

    class Meta:
        abstract = True


@receiver(models.signals.post_delete)
def post_delete_base_model_handler(sender, instance, *args, **kwargs):
    """Base post delete handler."""
    from apps.core import injector  # noqa: WPS433
    from apps.media.logic.interfaces import (  # noqa: WPS433
        ICleanupMediaFilesService,
    )

    if not isinstance(instance, BaseModel):
        return

    cleanup_service = injector.get(ICleanupMediaFilesService)
    cleanup_service.cleanup_media_files(instance)
