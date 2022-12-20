from django.db import models
from django.utils.translation import gettext_lazy as _


class Timestamps(models.Model):
    """Usefull timestamps fields mixin."""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("VN__CREATED_AT"),
        help_text=_("HT__CREATED_AT"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("VN__UPDATED_AT"),
        help_text=_("HT__UPDATED_AT"),
    )

    def __str__(self):
        """String representation."""
        return "created_at: {0}, updated_at: {1}".format(
            self.created_at,
            self.updated_at,
        )
