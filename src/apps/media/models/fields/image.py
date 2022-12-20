from django.db import models
from django.utils.translation import gettext_lazy as _


class ImageField(models.OneToOneField):
    """Image field."""

    def __init__(self, *args, **kwargs) -> None:
        """Init image field."""
        default_values = {
            "on_delete": models.SET_NULL,
            "null": True,
            "blank": True,
            "related_name": "+",
            "verbose_name": _("VN__IMAGE"),
            "help_text": _("HT__IMAGE"),
        }

        default_values.update(kwargs)
        kwargs = default_values
        kwargs["to"] = "media.Image"

        super().__init__(*args, **kwargs)
