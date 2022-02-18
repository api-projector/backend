import hashlib

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.models.fields import EnumField

from apps.core.models import BaseModel
from apps.core.models.mixins import Timestamps
from apps.media.models.fields import FileField


def assets_upload_to(project_asset, filename: str) -> str:
    """Generate folder for uploads."""
    project_hash = hashlib.md5(  # noqa: S303
        str(project_asset.project.pk).encode(),
    ).hexdigest()
    return "projects/{0}/{1}".format(project_hash, filename)


class ProjectAssetSource(models.TextChoices):
    """Project asset source."""

    FIGMA = "FIGMA", _("CH__FIGMA")  # noqa: WPS115
    UPLOAD = "UPLOAD", _("CH__UPLOAD")  # noqa: WPS115


class ProjectAsset(Timestamps, BaseModel):
    """Project asset model."""

    class Meta:
        verbose_name = _("VN__PROJECT_ASSET")
        verbose_name_plural = _("VN__PROJECTS_ASSETS")
        ordering = ("-created_at",)

    source = EnumField(
        enum=ProjectAssetSource,
        default=ProjectAssetSource.FIGMA,
        verbose_name=_("VN__PROJECT_ASSET_SOURCE"),
        help_text=_("HT__PROJECT_ASSET_SOURCE"),
    )

    file = FileField()  # noqa: WPS110
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("VN__PROJECT"),
        help_text=_("HT__PROJECT"),
    )

    def __str__(self):
        """Object present."""
        return self.source

    @property
    def file_url(self) -> str:
        """Returns file url with MEDIA prefix."""
        return "{0}{1}".format(settings.MEDIA_URL, self.file.path)
