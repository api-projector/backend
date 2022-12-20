from django.db import models
from django.utils.translation import gettext_lazy as _


class FileField(models.OneToOneField):
    """File field."""

    def __init__(self, *args, **kwargs) -> None:
        """Init file field."""
        default_values = {
            "on_delete": models.SET_NULL,
            "null": True,
            "blank": True,
            "related_name": "+",
            "verbose_name": _("VN__FILE"),
            "help_text": _("HT__FILE"),
        }

        default_values.update(kwargs)
        kwargs = default_values
        kwargs["to"] = "media.File"

        super().__init__(*args, **kwargs)
