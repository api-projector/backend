from django.contrib import admin
from jnt_django_toolbox.admin.mixins import AutocompleteAdminMixin


class BaseModelAdmin(
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""

    class Media:
        """Media."""

    list_per_page = 20
