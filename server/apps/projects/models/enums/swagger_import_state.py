from django.db import models
from django.utils.translation import gettext_lazy as _


class SwaggerImportState(models.TextChoices):
    """Swagger import state."""

    CREATED = "created", _("VN__CREATED")
    RUNNING = "running", _("VN__RINNING")
    FAILED = "failed", _("VN__FAILED")
    DONE = "done", _("VN__DONE")
