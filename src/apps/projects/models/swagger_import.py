from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.core.models.mixins import Timestamps
from apps.projects.models.enums import SwaggerImportState


class SwaggerImport(Timestamps, BaseModel):
    """Swagger import model."""

    class Meta:
        verbose_name = _("VN__SWAGGER_IMPORT")
        verbose_name_plural = _("VN__SWAGGER_IMPORT")

    state = models.TextField(
        blank=True,
        verbose_name=_("VN__STATE"),
        help_text=_("HT__STATE"),
        choices=SwaggerImportState.choices,
        default=SwaggerImportState.CREATED,
    )

    swagger_content = models.TextField(
        default="",
        blank=True,
        verbose_name=_("VN__SWAGGER_CONTENT"),
        help_text=_("HT__SWAGGER_CONTENT"),
    )

    swagger_url = models.TextField(
        default="",
        blank=True,
        verbose_name=_("VN__SWAGGER_URL"),
        help_text=_("HT__SWAGGER_URL"),
    )

    log = models.TextField(
        default="",
        blank=True,
        verbose_name=_("VN__LOG"),
        help_text=_("HT__LOG"),
    )

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        verbose_name=_("VN__PROJECT"),
        help_text=_("HT__PROJECT"),
        related_name="swagger_imports",
    )

    def __str__(self):
        """Text representation."""
        return "{0} [{1}]".format(self.project, self.state)
