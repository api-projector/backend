from django.contrib import admin
from django.contrib.auth.models import Group

from apps.core.admin.base import BaseModelAdmin

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    """Group admin."""

    list_display = ("name",)
    search_fields = ("name",)
